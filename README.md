# io-project-one
Projekt programu do zarządzania projektami w firmach programistycznych 

Do poprawnego działania programu niezbędne jest stworzenie bazy danych MariaDB o nazwie ioProjectOne, oraz dodanie nowego użytkownika, który będzie miał do niej dostęp:
User: projectOneUser
Password: VeryHardP@ssw0rd

Baza danych wymaga zaimportowania pliku ioProjectOne_07.06.dump, który znajduje się w folderze Database_dumps.

Program należy uruchomić przy pomocy pliku main.py.

Aby zalgować się do systemu trzeba skorzystać z domyślnego konta:
User: user1
Password: Password123
 
 W zakładce "Dodaj użytkownika" można dodać kolejnych pracowników, mających dostęp do systemu. Wymaga to wypełnienia wszystkich danych personalnych, utworzenia loginu i hasła, oraz uzupełnienia informacji dotyczących znanych języków programowania.
 
 Zakładka "Utworz projekt" umożliwia dodawanie nowych projektów oraz przypisanie do nich pracowników.
 Pracowników można wybrać ręcznie lub automatycznie - system sam dobierze pracowników na podstawie ich umiejętności.
 W menu głównym można usunąć wcześniej utworzone projekty.
 
 Program wymaga bibliotek:
 -pywebio
 -mariadb
 -numpy
