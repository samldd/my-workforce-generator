from datetime import datetime
import random
import json
import unicodedata


class Skill:

    def __init__(self, employee):
        self.employee = employee
        self.acquired = Skill.get_random_date()
        self.skillname, self.skilluri = self.get_random_skill()
        self.employee.add_skill(self)
        self.uuid = helpers.generate_uuid()

    def persist(self):
        q = """
        prefix esco: <http://data.europa.eu/esco/model#>
        prefix default: <http://example.org/MyCompany/>
        prefix mu: <http://mu.semte.ch/vocabularies/core/>

        INSERT DATA{
            GRAPH <http://mu.semte.ch/application> {
                default:%s_%s a default:EmployeeSkill;
                              esco:hasSkill <%s>;
                              default:acquired %s;
                              mu:uuid %s.
                default:%s default:hasSkill default:%s_%s.
            }
        }
        """ % (self.get_skill_name(), self.employee.get_name(), self.skilluri, sparql_escape(self.acquired),
               sparql_escape(self.uuid), self.employee.get_name(), self.get_skill_name(), self.employee.get_name())
        helpers.update(q)

    def get_random_skill(self):
        return random.choice(self.get_skill_pool())

    def get_skill_name(self):
        return self.skillname.translate(None, '/<>-_=+).,?\'\"(*&$#@!').replace(" ", "_")

    SKILLPOOL = []

    @classmethod
    def get_skill_pool(cls):
        """ Looks up all the esco skills under the 'ICT development' node, and returns
        all these skills together with an URI for each skill. """

        if len(Skill.SKILLPOOL) == 0:
            q = """
            prefix esco: <http://data.europa.eu/esco/model#>
            prefix skosxl: <http://www.w3.org/2008/05/skos-xl#>
            prefix skos: <http://www.w3.org/2004/02/skos/core#>

            SELECT distinct (str(?lit2) as ?skillLiteral) ?skill
                WHERE{
                    GRAPH <http://mu.semte.ch/application>{
                        ?topNode a esco:Skill.
                        ?topNode skosxl:prefLabel ?label.
                        ?label skosxl:literalForm ?lit.
                        FILTER regex(str(?lit),"ICT development").
                        ?skill skos:broader* ?topNode.
                        ?skill skosxl:prefLabel ?label2.
                        ?label2 skosxl:literalForm ?lit2.
                        FILTER NOT EXISTS { ?o skos:broader ?skill }.
                    }
            }"""
            data = helpers.query(q)
            bindings = data["results"]["bindings"]
            for b in bindings:
                name = b["skillLiteral"]["value"]
                name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
                uri = b["skill"]["value"]
                Skill.SKILLPOOL.append([name.replace(" ", "_"), uri])
        return Skill.SKILLPOOL

    @classmethod
    def get_random_date(cls):
        """ Generate a random date between 1/1/2008 and 1/1/2016."""
        form = '%d/%m/%Y'
        start = datetime.strptime("1/1/2008", form).toordinal()
        end = datetime.strptime("1/1/2016", form).toordinal()
        num = random.uniform(0, 1)
        new = start + (end-start)*num
        return datetime.fromordinal(int(new)).date()

