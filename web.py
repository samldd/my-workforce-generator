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


def generate_employee():
    emp = Employee()
    for _ in range(0, random.randint(10, 20)):
        Skill(emp)
    Occupation(emp)
    return emp
