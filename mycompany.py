
class Mycompany():

    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        self.uuid = helpers.generate_uuid()
        employee.add_company(self)

    def persist(self):
        q = """
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix default: <http://example.org/MyCompany/>
            prefix mu: <http://mu.semte.ch/vocabularies/core/>

            INSERT DATA{
                GRAPH <http://mu.semte.ch/application> {
                    default:MyCompany rdfs:label "MyCompanyName";
                                        mu:uuid %s.

                }
            }
            """ % sparql_escape(self.uuid)
        helpers.update(q)
        for e in self.employees:
            e.persist()

    @classmethod
    def get_URI(cls):
        return "http://example.org/MyCompany/MyCompany"

    def get_company_state(self):
        s = "The Company has hired the following people: \n"
        for p in self.employees:
            s += p.get_name() + "\n"
        return s
