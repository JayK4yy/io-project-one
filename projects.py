import mariadb
from pywebio.input import *
from pywebio.output import *
from hash import connect_database
from numpy import asarray
from functools import partial


conn = connect_database()


@use_scope('projects')
def show_projects():
    set_scope('projects')
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT 
        projectNumber,
        projectTitle,
        CONCAT_WS(' ', firstName, lastName) as 'leader_name',
        progress,
        deadline
    FROM Projects JOIN Employees
    ON Projects.projectLeader = Employees.employeeNumber
    ORDER BY projectNumber;
    """)
    lst = cursor.fetchall()  # pobierz liste
    for i in range(len(lst)):
        lst[i] = [lst[i][0], lst[i][1], lst[i][2], lst[i][3], lst[i][4],
                  # put_buttons(['Delete', 'Show'], onclick=[partial(deleteProject, i), partial(showProject, i)])]
                  put_buttons(['Delete'], onclick=partial(deleteProject, i))]
    put_table(lst, header=['Numer', 'Tytuł projektu', 'Kierownik projektu', 'Postępy prac', 'Deadline', 'Akcje'])


def addProjectOnly(data_dodaj):
    cursor = conn.cursor()
    cursor.execute("""SELECT MAX(projectNumber) FROM projects""")
    projectNumber = cursor.fetchall()[0][0] + 1
    query_add_project = """INSERT INTO Projects(projectNumber,projectLeader,status,
                                deadline,projectTitle,progress) VALUES (%d,%d,%s,%s,%s,%s)"""
    values_add_project = (projectNumber, data_dodaj['reportsTo'], 'New',
                          data_dodaj['deadline'], data_dodaj['projectTitle'], '0%')
    cursor.execute(query_add_project, values_add_project)
    conn.commit()


def chooseEmployeesAuto(data_dodaj, employees_data):
    skills_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for skill in employees_data['skille']:
        if skill == 'C':
            skills_array[0] = 1
        elif skill == 'C++':
            skills_array[1] = 1
        elif skill == 'C#':
            skills_array[2] = 1
        elif skill == 'Python':
            skills_array[3] = 1
        elif skill == 'Java':
            skills_array[4] = 1
        elif skill == 'HTML':
            skills_array[5] = 1
        elif skill == 'CSS':
            skills_array[6] = 1
        elif skill == 'JavaScript':
            skills_array[7] = 1
        elif skill == 'SQL':
            skills_array[8] = 1
        elif skill == 'PHP':
            skills_array[9] = 1

    cursor = conn.cursor()
    cursor.execute("""SELECT Employees.employeeNumber, skills.c,skills.cpp,skills.cs,
    skills.python,skills.java,skills.html,skills.css,skills.javascript,
    skills.sqlskill,skills.php,0
    FROM employees JOIN skills ON  employees.employeeNumber=skills.employeeNumber""")

    employeesskills = asarray(cursor.fetchall())
    j = -1
    for row in employeesskills:
        j += 1
        for k in range(len(skills_array)):
            if skills_array[k] == 1 and row[k + 1] == 1:
                employeesskills[j][11] += 1

    employeesskills = employeesskills.tolist()
    employeesskills.sort(key=lambda x: x[11], reverse=True)

    # for employee in employeesskills:
    #     print(employee)

    cursor.execute("""SELECT COUNT(*) FROM employees""")
    maxEmployees = cursor.fetchall()[0][0]

    if employees_data['employeesNumber'] > maxEmployees:
        employees_data['employeesNumber'] = maxEmployees - 1
    print(employees_data['employeesNumber'])

    cursor.execute("""SELECT MAX(projectNumber) FROM projects""")
    projectNumber = cursor.fetchall()[0][0] + 1
    query_add_project = """INSERT INTO Projects(projectNumber,projectLeader,status,
                            deadline,projectTitle,progress) VALUES (%d,%d,%s,%s,%s,%s)"""
    values_add_project = (projectNumber, data_dodaj['reportsTo'], 'New',
                          data_dodaj['deadline'], data_dodaj['projectTitle'], '0%')
    cursor.execute(query_add_project, values_add_project)
    conn.commit()

    query_employee_project = """INSERT INTO teams(employeeNumber,projectNumber,role) VALUES (%d,%d,%s)"""
    for k in range(employees_data['employeesNumber']):
        values_employee_project = (employeesskills[k][0], projectNumber, 'programista')
        cursor.execute(query_employee_project, values_employee_project)
    conn.commit()


def chooseEmployeesManual(data_dodaj, employees_data):
    cursor = conn.cursor()

    cursor.execute("""SELECT MAX(projectNumber) FROM projects""")
    projectNumber = cursor.fetchall()[0][0] + 1
    query_add_project = """INSERT INTO Projects(projectNumber,projectLeader,status,
                                deadline,projectTitle,progress) VALUES (%d,%d,%s,%s,%s,%s)"""
    values_add_project = (projectNumber, data_dodaj['reportsTo'], 'New',
                          data_dodaj['deadline'], data_dodaj['projectTitle'], '0%')
    cursor.execute(query_add_project, values_add_project)
    conn.commit()

    query_employee_project = """INSERT INTO teams(employeeNumber,projectNumber,role) VALUES (%d,%d,%s)"""
    for employee in employees_data:
        values_employee_project = (employee, projectNumber, 'programista')
        cursor.execute(query_employee_project, values_employee_project)
    conn.commit()


def addAutomatically(data_dodaj):
    employees_data = input_group("Pracownicy", [
        input('Liczba pracowników:', name='employeesNumber', type=NUMBER),
        checkbox('Wymagane umiejetności:', ['C', 'C++', 'C#', 'Python', 'Java', 'HTML',
                                            'CSS', 'JavaScript', 'SQL', 'PHP'], name='skille'),

        actions('', [
            {'label': 'Zapisz', 'value': 'save'},
            {'label': 'Anuluj', 'value': 'cancel'},
        ], name='action'), ])

    if employees_data['action'] == 'save':
        chooseEmployeesAuto(data_dodaj, employees_data)
        print(employees_data['skille'])
    elif employees_data['action'] == 'cancel':
        return


def addManually(data_dodaj):
    cursor = conn.cursor()
    cursor.execute("""  SELECT CONCAT_WS(' ', firstName, lastName) as 'employeeName', employeeNumber
                        FROM Employees WHERE jobTitle != 'admin' ORDER BY employeeNumber; """)
    pracownicy = cursor.fetchall()

    pracownicy_wybor = input_group("Dodawanie pracowników do projektu", [
        checkbox('', pracownicy, name='pracownicy_checkboxy'),

        actions('', [
            {'label': 'Zapisz', 'value': 'save'},
            {'label': 'Anuluj', 'value': 'cancel'},
        ], name='action'),
    ])

    if pracownicy_wybor['action'] == 'save':
        chooseEmployeesManual(data_dodaj, pracownicy_wybor['pracownicy_checkboxy'])
    elif pracownicy_wybor['action'] == 'cancel':
        return


def deleteProject(number, choice):
    cursor = conn.cursor()
    number = int(number)
    number = number + 1
    number = str(number)
    cursor.execute("DELETE FROM Teams WHERE projectNumber = ?;", (number,))
    cursor.execute("DELETE FROM Projects WHERE projectNumber = ?;", (number,))
    conn.commit()
    popup(str('Event ' + str(number) + ' deleted!'), size=PopupSize.SMALL)
    # print(choice, number)
    remove('projects')
    show_projects()


def addProject():
    cursor = conn.cursor()
    cursor.execute("SELECT CONCAT_WS(' ',firstName,lastName),employeeNumber "
                   "FROM Employees WHERE jobTitle = 'kierownik'")
    kierownicy = cursor.fetchall()

    data_dodaj = input_group("Dodawanie projektu", [
        input('Tytuł projektu', name='projectTitle'),
        select('Kierownik projektu', kierownicy, name='reportsTo'),
        input('Termin wykonania', name='deadline', type=DATE),
        radio("Jak chcesz dobrać pracowników do projektu:", ['manualnie', 'automatycznie'], name='wybor'),

        actions('', [
            {'label': 'Zapisz i wybierz pracowników', 'value': 'zapisz'},
            {'label': 'Anuluj', 'value': 'cancel'}
        ], name='action'),
    ])

    try:
        if data_dodaj['action'] == 'zapisz' and data_dodaj['wybor'] == 'automatycznie':
            addAutomatically(data_dodaj)
            return
        elif data_dodaj['action'] == 'zapisz' and data_dodaj['wybor'] == 'manualnie':
            addManually(data_dodaj)
            return
        elif data_dodaj['action'] == 'zapisz' and data_dodaj['wybor'] is None:
            addProjectOnly(data_dodaj)
            return
        elif data_dodaj['action'] == 'cancel':
            return
    except mariadb.Error:
        put_error('Błędne dane!')
        addProject()
