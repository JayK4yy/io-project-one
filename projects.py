import pywebio.session
from pywebio.input import *
from pywebio.output import *
from hash import connect_database, hash_login
from numpy import asarray


conn = connect_database()


def addSQL(data):
        skills = ['C', 'Cpp', 'Cs', 'Python', 'Java', 'HTML', 'CSS', 'JavaScript', 'SQL', 'PHP']

        for skill in skills:
            if data[skill] == 'Tak':
                data[skill] = 1
            elif data[skill] == 'Nie':
                data[skill] = 0
        if data['reportsTo'] == 'Jakub Paszkiewicz':
            data['reportsTo'] = 1
        elif data['reportsTo'] == 'Kacper Kubicki':
            data['reportsTo'] = 2

        cursor = conn.cursor()
        cursor.execute("SELECT MAX(employeeNumber) FROM employees")
        userID = cursor.fetchall()[0][0] + 1

        # Dodajemy do pracownikow
        query_user = """INSERT INTO employees(employeeNumber,lastName,firstName,office,
                                    jobTitle,city,postalCode,adress,phone,gender,email,reportsTo)
                        VALUES (%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d) """
        values_user = (userID, data['lastName'], data['firstName'], data['office'],
                       data['jobTitle'], data['city'], data['postalCode'], data['adress'],
                       data['phone'], data['gender'], data['email'], data['reportsTo'])
        cursor.execute(query_user, values_user)

        # Dodajemy do skilli
        query_skills = """  INSERT INTO skills(employeeNumber,c,html,css,java,python,javascript,cs,sqlskill,php,cpp) 
                            VALUES (%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)"""
        values_skills = (
            userID, data['C'], data['HTML'], data['CSS'], data['Java'], data['Python'], data['JavaScript'],
            data['Cs'], data['SQL'], data['PHP'], data['Cpp'])
        cursor.execute(query_skills, values_skills)

        salt, key = hash_login(data['password'])
        salt = str(salt)
        key = str(key)
        query_login = """INSERT INTO authentication(employeeNumber,login,pass_key,salt) VALUES (%d,%s,%s,%s) """
        values_login = (userID, data['login'], key, salt)
        cursor.execute(query_login, values_login)

        conn.commit()


def addProject():
    def addAutomatically(data_dodaj):
        def chooseEmployees(data_dodaj, employees_data):

            skills = ['C', 'Cpp', 'Cs', 'Python', 'Java', 'HTML', 'CSS', 'JavaScript', 'SQL', 'PHP']

            for skill in skills:
                if employees_data[skill] == 'Tak':
                    employees_data[skill] = 1
                elif employees_data[skill] == 'Nie':
                    employees_data[skill] = 0

            cursor = conn.cursor()
            cursor.execute("""SELECT Employees.employeeNumber, skills.c,skills.cpp,skills.cs,skills.python,skills.java,skills.html,skills.css,skills.javascript,
            skills.sqlskill,skills.php,0 
            FROM employees JOIN skills ON  employees.employeeNumber=skills.employeeNumber""")

            employeesskills = asarray(cursor.fetchall())
            j = -1
            for row in employeesskills:
                j += 1
                for i in range(len(skills)):
                    if employees_data[skills[i]] == 1 and row[i + 1] == 1:
                        employeesskills[j][11] += 1



            employeesskills = employeesskills.tolist()
            employeesskills.sort(key=lambda x: x[11], reverse=True)

            cursor.execute("""SELECT COUNT(*) FROM employees""")
            maxEmployees = cursor.fetchall()[0][0]

            if employees_data['employeesNumber'] > maxEmployees:
                employees_data['employeesNumber'] = maxEmployees - 1
            print(employees_data['employeesNumber'])

            cursor.execute("""SELECT MAX(projectNumber) FROM projects""")
            projectNumber = cursor.fetchall()[0][0] + 1
            query_add_project = """INSERT INTO projects(projectNumber,projectLeader,status,deadline,projectTitle,progress) VALUES (%d,%d,%s,%s,%s,%s)"""
            values_add_project = (
            projectNumber, data_dodaj['reportsTo'], 'New', data_dodaj['deadline'], data_dodaj['projectTitle'],'0%')
            cursor.execute(query_add_project, values_add_project)
            conn.commit()

            query_employee_project="""INSERT INTO teams(employeeNumber,projectNumber,role) VALUES (%d,%d,%s)"""
            for i in range(employees_data['employeesNumber']):
                values_employee_project=(employeesskills[i][0],projectNumber,'programista')
                cursor.execute(query_employee_project, values_employee_project)
            conn.commit()


        employees_data = input_group("Pracownicy", [
            input('Liczba pracowników', name='employeesNumber', type=NUMBER),
            radio('C', options=['Tak', 'Nie'], name='C'),
            radio('C++', options=['Tak', 'Nie'], name='Cpp'),
            radio('C#', options=['Tak', 'Nie'], name='Cs'),
            radio('Python', options=['Tak', 'Nie'], name='Python'),
            radio('Java', options=['Tak', 'Nie'], name='Java'),
            radio('HTML', options=['Tak', 'Nie'], name='HTML'),
            radio('CSS', options=['Tak', 'Nie'], name='CSS'),
            radio('JavaScript', options=['Tak', 'Nie'], name='JavaScript'),
            radio('SQL', options=['Tak', 'Nie'], name='SQL'),
            radio('PHP', options=['Tak', 'Nie'], name='PHP'),

            actions('', [
                {'label': 'Zapisz', 'value': 'save'},
                {'label': 'Anuluj', 'value': 'cancel'},
            ], name='action'), ])

        if employees_data['action'] == 'save':
            chooseEmployees(data_dodaj, employees_data)
        elif employees_data['action'] == 'cancel':
            return

    cursor = conn.cursor()
    cursor.execute("SELECT CONCAT_WS(' ',firstName,lastName),employeeNumber FROM Employees WHERE jobTitle = 'kierownik'")
    kierownicy = cursor.fetchall()
    cursor.execute("SELECT CONCAT_WS(' ',firstName,lastName),employeeNumber FROM Employees WHERE jobTitle = 'kierownik'")
    kierownicyID=cursor.fetchall()
    for i in range(len(kierownicy)):
        kierownicy[i] = kierownicy[i][0]
    print(kierownicyID[0][0])


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
    j=-1
    for kierownik in kierownicyID:
        j+=1
        if data_dodaj['reportsTo']==kierownik[0]:
            data_dodaj['reportsTo']=kierownik[1]
    print(data_dodaj['reportsTo'])

    if data_dodaj['action'] == 'zapisz' and data_dodaj['wybor']=='automatycznie':
        addAutomatically(data_dodaj)
        return
        # main_menu()
    elif data_dodaj['action'] == 'cancel':
        # main_menu()
        return


def addEmployeesToProject():
    data_to_add = input_group("Dodawanie pracowników do projektu", [
        actions('', [
            {'label': 'Manualne dobieranie', 'value': 'manual'},
            {'label': 'Automatyczne dobieranie', 'value': 'automatic'}
        ], name='action_dobieranie')
    ])
