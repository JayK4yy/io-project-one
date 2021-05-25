from pywebio.input import *
from pywebio.output import *


def main():
    put_table([
        ['Projekty', ''],
        ['Projek1', put_buttons(['Okno projektu'], onclick=...)],
        ['Projek2', put_buttons(['Okno projektu'], onclick=...)],
    ])


def podajpracownika():
    dane = input_group("Dodawanie pracownika", [
        input('Imię', name='firstName'),
        input('Nazwisko', name='lastName'),
        input('Adres e-mail', name='email'),
        radio('Płeć', options=['M', 'K'], name='gender'),
        input('Numer telefonu', type=NUMBER, name='phone'),
        input('Ulica', name='adress'),
        input('Kod pocztowy', name='postalCode'),
        input('Miasto', name='city'),
        input('Stanowisko', name='jobTitle'),
        input('Biuro', name='office'),
        input('Przełożony', name='reportsTo'),

        # umiejętności
        radio('C', options=['Tak', 'Nie'], name='C'),
        radio('C++', options=['Tak', 'Nie'], name='Cpp'),
        radio('Python', options=['Tak', 'Nie'], name='Python'),
        radio('Java', options=['Tak', 'Nie'], name='Java')
    ])
    put_text(dane)


if __name__ == '__main__':
    podajpracownika()


