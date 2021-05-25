import mariadb
from pywebio.input import *
from pywebio.output import *


def main():
    mainmenu = input_group("Strona główna ", [actions('', [
            {'label': 'Dodaj pracownika', 'value': 'addEmployee'},
            {'label': 'Utwórz projekt', 'value': 'CreateProject'},
            {'label': 'Wyloguj', 'value': 'logout'},
        ], name='action'),
    ])
    if mainmenu['action'] == 'addEmployee':
        addEmployee()
    elif mainmenu['action'] == 'CreateProject':
        print('bb')
    elif mainmenu['action'] == 'logout':
        print('Wylogowano')
        exit()


def addEmployee():
    data = input_group("Dodawanie pracownika", [
        input('Imię', name='firstName'),
        input('Nazwisko', name='lastName'),
        input('Adres e-mail', name='email'),
        radio('Płeć', options=['M', 'K'], name='gender'),
        input('Numer telefonu', name='phone'),
        input('Ulica', name='adress'),
        input('Kod pocztowy', name='postalCode'),
        input('Miasto', name='city'),
        input('Stanowisko', name='jobTitle'),
        input('Biuro', name='office'),
        input('Przełożony', name='reportsTo'),
        input('Hasło', name='password'),

        # umiejętności
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
            {'label': 'Anuluj', 'value': 'cancel'}
        ], name='action'),
    ])
    if data['action'] == 'save':
        main()
    elif data['action'] == 'cancel':
        main()


def login():

    logindata = input_group("Logowanie", [
        input('Login', name='login'),
        input('Hasło', name='password')])

    try:
        conn = mariadb.connect(
            user=logindata['login'],
            password=logindata['password'],
            host="localhost",
            port=3306,
        )

        cur = conn.cursor()
        cur.execute("USE ioProjectOne")
        cur.execute("SELECT * FROM Employees")
    except:
        put_error('Błędne dane')
        login()


if __name__ == '__main__':
    login()
    main()
