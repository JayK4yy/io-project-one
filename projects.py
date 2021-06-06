from pywebio.input import *
from pywebio.output import *
from hash import connect_database, hash_login


conn = connect_database()


def addSQL(data):
    # Tutaj tylko wartosci zmieniamy zeby nie bylo Tak/Nie
    if data['login'] != '' and data['password'] != '':
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
    else:
        put_error('Błędne dane')
        addProject()


def addProject():
    cursor = conn.cursor()
    cursor.execute("SELECT CONCAT_WS(' ',firstName,lastName) FROM Employees WHERE jobTitle = 'kierownik'")
    kierownicy = cursor.fetchall()
    for i in range(len(kierownicy)):
        kierownicy[i] = kierownicy[i][0]

    data_dodaj = input_group("Dodawanie projektu", [
        input('Tytuł projektu', name='projectTitle'),
        select('Kierownik projektu', kierownicy, name='reportsTo'),
        input('Termin wykonania', name='deadline', type=DATE),

        actions('', [
            {'label': 'Zapisz', 'value': 'save'},
            {'label': 'Anuluj', 'value': 'cancel'}
        ], name='action'),
    ])

    if data_dodaj['action'] == 'save':
        addSQL(data_dodaj)
        return
        # main_menu()
    elif data_dodaj['action'] == 'cancel':
        # main_menu()
        return
