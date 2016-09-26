from datetime import datetime
import random
import unicodedata


class Occupation:

    def __init__(self, employee):
        self.employee = employee
        self.acquired = self.get_random_date()
        self.occname, self.occuri = self.get_random_occupation()
        self.employee.add_occupation(self)
        self.uuid = helpers.generate_uuid()

    def persist(self):
        helpers.log("************* DEBUG ********* ")
        helpers.log(type(self.acquired))
        q = """
            prefix esco: <http://data.europa.eu/esco/model#>
            prefix default: <http://example.org/MyCompany/>
            prefix mu: <http://mu.semte.ch/vocabularies/core/>

            INSERT DATA{
                GRAPH <http://mu.semte.ch/application> {
                    default:%s_%s a default:EmployeeFunction;
                                  esco:hasOccupation <%s>;
                                  default:startDate %s;
                                  mu:uuid %s.
                    default:%s default:function default:%s_%s.
                }
            }
            """ % (self.get_occ_name(), self.employee.get_name(), self.occuri, sparql_escape(self.acquired),
        sparql_escape(self.uuid), self.employee.get_name(), self.get_occ_name(), self.employee.get_name())

        helpers.update(q)

    def get_random_occupation(self):
        return random.choice(self.get_occupation_pool())

    def get_occ_name(self):
        return self.occname.translate(None, '/<>-_=+)(*&$.,\'\"?#@!').replace(" ", "_")

    OCCUPATION_POOL = []

    @classmethod
    def get_occupation_pool(cls):
        """ Looks up all the esco occupations under the 'ICT development' node, and returns
        all these occupations together with an URI for each skill. """
        if len(Occupation.OCCUPATION_POOL) == 0:
            q = """
                prefix esco: <http://data.europa.eu/esco/model#>
                prefix skosxl: <http://www.w3.org/2008/05/skos-xl#>
                prefix skos: <http://www.w3.org/2004/02/skos/core#>

                SELECT distinct (str(?lit2) as ?occupationLiteral) ?occ
                    WHERE{
                        GRAPH <http://mu.semte.ch/application>{
                            ?topNode a esco:Occupation.
                            ?topNode skosxl:prefLabel ?label.
                            ?label skosxl:literalForm ?lit.
                            FILTER regex(str(?lit),"ICT development").
                            ?occ skos:broader* ?topNode.
                            ?occ skosxl:prefLabel ?label2.
                            ?label2 skosxl:literalForm ?lit2.
                            FILTER NOT EXISTS { ?o skos:broader ?occ }.
                        }
                }"""
            data = helpers.query(q)
            bindings = data["results"]["bindings"]
            for b in bindings:
                name = b["occupationLiteral"]["value"]
                name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
                uri = b["occ"]["value"]
                Occupation.OCCUPATION_POOL.append([name.replace(" ", "_"), uri])
        return Occupation.OCCUPATION_POOL

    @classmethod
    def get_random_date(cls):
        """ Generate a random date between 1/1/2008 and 1/1/2016."""
        form = '%d/%m/%Y'
        start = datetime.strptime("1/1/2008", form).toordinal()
        end = datetime.strptime("1/1/2016", form).toordinal()
        num = random.uniform(0, 1)
        new = start + (end - start) * num
        return datetime.fromordinal(int(new)).date()
