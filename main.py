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
    def addSQL(data):
        #Tutaj tylko wartosci zmieniamy zeby nie bylo Tak/Nie
        skills=['C','Cpp','Cs','Python','Java','HTML','CSS','JavaScript','SQL','PHP']

        for skill in skills:
            if data[skill]=='Tak':
                data[skill]=1
            elif data[skill]=='Nie':
                data[skill]=0

        #Laczymy sie z baza(przyda sie zrobic do tego funckje)
        conn = mariadb.connect(
            user='projectOneUser',
            password='VeryHardP@ssw0rd',
            host="localhost",
            port=3306,
            database="ioProjectOne"
        )


        cursor = conn.cursor()
        cursor.execute("SELECT MAX(employeeNumber) FROM employees")
        userID=cursor.fetchall()[0][0]+1

        #Dodajemy do pracownikow
        query_user="""INSERT INTO employees(employeeNumber,lastName,firstName,office,jobTitle,city,postalCode,adress,phone,gender,email)
                       VALUES (%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        values_user=(userID,data['lastName'],data['firstName'],data['office'],data['jobTitle'],data['city'],data['postalCode'],data['adress'],data['phone'],
                data['gender'],data['email'])
        cursor.execute(query_user, values_user)

       #Dodajemy do skilli
        query_skills = """INSERT INTO skills(employeeNumber,c,html,css,java,python,javascript,cs,sqlskill,php,cpp) VALUES (%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)"""
        values_skills = (
            userID,data['C'],  data['Python'], data['Java'], data['HTML'], data['CSS'],data['JavaScript'],data['Cs'],data['SQL'],data['PHP'],data['Cpp'])
        cursor.execute(query_skills, values_skills)

        conn.commit()




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
        addSQL(data)
        main()
    elif data['action'] == 'cancel':
        main()


def login():

    logindata = input_group("Logowanie", [
        input('Login', name='login'),
        input('Hasło',type=PASSWORD, name='password')])

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
