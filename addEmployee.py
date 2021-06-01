import mariadb
from pywebio.input import *
from login import *
from main import *

def addEmployee():
    def addSQL(data):
        #Tutaj tylko wartosci zmieniamy zeby nie bylo Tak/Nie
        if data['login'] != '' and data['password']!='':
            skills=['C','Cpp','Cs','Python','Java','HTML','CSS','JavaScript','SQL','PHP']

            for skill in skills:
                if data[skill]=='Tak':
                    data[skill]=1
                elif data[skill]=='Nie':
                    data[skill]=0
            if data['reportsTo']=='Jakub Paszkiewicz':
                data['reportsTo']=1
            elif data['reportsTo']=='Kacper Kubicki':
                data['reportsTo'] = 2

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
            query_user="""INSERT INTO employees(employeeNumber,lastName,firstName,office,jobTitle,city,postalCode,adress,phone,gender,email,reportsTo)
                           VALUES (%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d) """
            values_user=(userID,data['lastName'],data['firstName'],data['office'],data['jobTitle'],data['city'],data['postalCode'],data['adress'],data['phone'],
                    data['gender'],data['email'], data['reportsTo'])
            cursor.execute(query_user, values_user)

           #Dodajemy do skilli
            query_skills = """INSERT INTO skills(employeeNumber,c,html,css,java,python,javascript,cs,sqlskill,php,cpp) VALUES (%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)"""
            values_skills = (
                userID,data['C'],  data['HTML'], data['CSS'], data['Java'], data['Python'],data['JavaScript'],data['Cs'],data['SQL'],data['PHP'],data['Cpp'])
            cursor.execute(query_skills, values_skills)


            salt,key=hash_login(data['password'])
            salt=str(salt)
            key=str(key)
            query_login="""INSERT INTO authentication(employeeNumber,login,pass_key,salt) VALUES (%d,%s,%s,%s) """
            values_login=(userID,data['login'],key,salt)
            cursor.execute(query_login, values_login)


            conn.commit()
        else:
            put_error('Błędne dane')
            addEmployee()




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
        select('Przełożony', ['Jakub Paszkiewicz','Kacper Kubicki'], name='reportsTo'),
        input('Login', name='login'),
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
