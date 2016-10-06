import json
import random
from mycompany import Mycompany

class Employee():

    FRONTNAMES = ["Sam", "Arno", "Johan", "Nora", "Karel", "Aad", "Erica", "Vincent", "Jonathan", "Niels", "Jan", "Piet", "Brecht", "Yannick", "Cieltje", "Amber", "Katelijne", "Adriaan", "Charlotte"]
    LASTNAMES = ["Landuydt", "Versteden", "Kremer", "De Smedt", "Vandekeybus", "Fannes", "Maes", "Janssens", "Van de bosch", "Billen", "Barbier", "De Bruyn", "Mertens", "Andries"]

    def __init__(self):
        """ Neem een willekeurige naam uit de front en last names en controlleer of
        deze naam nog beschikbaar is. Zo niet, genereer een andere naam. """
        front = random.choice(self.FRONTNAMES)
        last = random.choice(self.LASTNAMES)
        while not self.check_occurence(front, last):
            front = random.choice(self.FRONTNAMES)
            last = random.choice(self.LASTNAMES)
        self.front = front
        self.last = last
        self.skills = []
        self.company = None
        self.occupation = None
        self.uuid = helpers.generate_uuid()
        self.persisted = False

    def add_company(self, company):
        self.company = company

    def add_skill(self, new_skill):
        """ Checks whether the employee has the skill already acquired,
        if not, it is added to the employees skill set. """
        s = new_skill.get_skill_name()
        for skill in self.skills:
            if skill.get_skill_name() == s:
                return None
        self.skills.append(new_skill)

    def add_occupation(self, occupation):
        """Voorlopig krijgt elke persoon maar 1 occupation"""
        self.occupation = occupation

    @classmethod
    def check_occurence(cls, front, last):
        q = """
        prefix foaf: <http://xmlns.com/foaf/spec/>

        SELECT distinct (str(?n) as ?employeeName)
        WHERE{
          GRAPH <http://localhost:8890/MyWorkForce> {
            ?p foaf:name ?n.
            FILTER regex(str(?n), %s)
          }
        }
        """ % sparql_escape(front + " " + last)
        data = helpers.query(q)
        bindings = data["results"]["bindings"]
        for b in bindings:
            name = b["employeeName"]["value"]
            if not name:
                return False
        return True

    def persist(self):
        if self.persisted:
            return
        front = self.front
        last = self.last
        if not self.occupation or not self.company:
            raise Exception("Employee has no occupation.")
        q = """
            prefix foaf: <http://xmlns.com/foaf/spec/>
            prefix default: <http://example.org/MyCompany/>
            prefix mu: <http://mu.semte.ch/vocabularies/core/>

            INSERT DATA{
                GRAPH <http://mu.semte.ch/application>{
                    default:%s a default:Employee;
                                 foaf:name %s;
                                 default:worksFor <%s>;
                                 mu:uuid %s.
                }
            }
        """ %(self.get_name(), sparql_escape(front + " " + last), Mycompany.get_URI(), sparql_escape(self.uuid))
        helpers.update(q)
        self.occupation.persist()
        for s in self.skills:
            s.persist()
        self.persisted = True

    def get_name(self):
        return self.front.replace(" ", "_") + "_" + self.last.replace(" ", "_")
