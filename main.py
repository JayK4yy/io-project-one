import mariadb
from pywebio.input import *
from pywebio.output import *
from employees import addEmployee
from login import login_veryfication


def connect_database():
    connection = mariadb.connect(
        user='projectOneUser',
        password='VeryHardP@ssw0rd',
        host="localhost",
        port=3306,
        database="ioProjectOne"
    )
    return connection


def main_menu():
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


def login():

    logindata = input_group("Logowanie", [
        input('Login', name='login'),
        input('Hasło', type=PASSWORD, name='password')])

    try:
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

    except IndexError:
        put_error('Błędny login')
        login()
    except ValueError:
        put_error('Błędne hasło')
        login()


if __name__ == '__main__':
    try:
        conn = connect_database()
        login()
        main_menu()
        # addEmployee()
    except mariadb.Error:
        put_error('Błąd połączenia z bazą danych')
