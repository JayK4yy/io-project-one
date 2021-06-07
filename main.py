import mariadb
from pywebio.input import *
from pywebio.output import *
import employees
import projects
from hash import login_veryfication, connect_database


def main_menu():
    while True:
        clear()

        with open('header_style.html', 'r') as file:
            header_style = file.read()

        with use_scope('header'):
            put_html(header_style)

        remove('projects')
        projects.show_projects()

        mainmenu = input_group("Strona główna ", [actions('', [
                {'label': 'Dodaj pracownika', 'value': 'addEmployee'},
                {'label': 'Utwórz projekt', 'value': 'CreateProject'},
                {'label': 'Wyloguj', 'value': 'logout'},
            ], name='action'),
        ])
        if mainmenu['action'] == 'addEmployee':
            remove('projects')
            employees.addEmployee()
        elif mainmenu['action'] == 'CreateProject':
            remove('projects')
            projects.addProject()
        elif mainmenu['action'] == 'logout':
            remove('projects')
            print('Wylogowano')
            with use_scope('projects'):
                put_text("WYLOGOWANO")
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
        # weryfikacja danych (funkcja z pliku hash.py)
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
