import mariadb
from pywebio.input import *
from pywebio.output import *
from login import *


def main():
    clear()
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
            user='projectOneUser',
            password='VeryHardP@ssw0rd',
            host="localhost",
            port=3306,
            database="ioProjectOne"
        )

        cursor = conn.cursor()
        # odczytujemy z bazy danych 'key' i 'salt' dla użytkokwnika o wpisanym loginie
        # jeśli login nie istnieje to wyskoczy komunikat 'błędne dane'
        cursor.execute("SELECT pass_key, salt FROM Authentication WHERE login = ?", (logindata['login'],))
        lst = cursor.fetchall()     # pobierz liste
        key = lst[0][0]             # pierwszy result -> key
        salt = lst[0][1]            # drugi result -> salt
        key = key.decode('unicode-escape').encode('ISO-8859-1')
        salt = salt.decode('unicode-escape').encode('ISO-8859-1')
        # weryfikacja danych (funkcja z pliku login.py)
        login_veryfication(salt[2:-1], key[2:-1], logindata['password'])


    except:
        put_error('Błędne dane')
        login()


if __name__ == '__main__':
    login()
    main()
