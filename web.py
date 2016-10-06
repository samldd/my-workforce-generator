"""
  Generate skills within a development context. All skills and occupations under the 'ICT development' node
   of the ESCO skill classification tree are used.
"""
from mycompany import Mycompany
from employee import Employee
from occupation import Occupation
from skill import Skill
import random

company = Mycompany()


@app.route('/generate-company/')
def job_pool():
    """ Generate a company with 20 employees and persist the company. """
    for _ in range(0, 20):
        company.add_employee(generate_employee())
    company.persist()
    return company.get_company_state().replace("\n", "<br>")


@app.route('/hire-person/')
def hirePerson():
    emp = Employee()
    for _ in range(0, random.randint(10, 20)):
        Skill(emp)
    Occupation(emp)
    emp.add_company(company)
    emp.persist()
    return emp.get_name() + " Is hired!"

@app.route('/add-labels/')
def label_concepts():
    q = """
    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    INSERT {
        GRAPH <http://mu.semte.ch/application> {
            ?s skos:prefLabel ?text.
        }
    } WHERE {
        ?s skosxl:prefLabel / skosxl:literalForm ?text.
        FILTER (lang(?text) = "en")
    }"""
    helpers.update(q)

def generate_employee():
    emp = Employee()
    for _ in range(0, random.randint(10, 20)):
        Skill(emp)
    Occupation(emp)
    return emp
