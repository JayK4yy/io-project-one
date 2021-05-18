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
        input('Imię', name='imie'),
        input('Nazwisko', name='nazwisko'),
        input('Data urodzenia', name='data_urodzenia'),
        radio('Płeć', options=['M', 'K'], name='plec'),
        input('Numer telefonu', type=NUMBER, name='phone'),
        input('Adres e-mail', name='email'),
        input('Miasto', name='miasto'),
        input('Kod pocztowy', name='postcode'),
        input('Ulica', name='ulica'),
        radio('C', options=['Tak', 'Nie'], name='C'),
        radio('C++', options=['Tak', 'Nie'], name='Cpp'),
        radio('Python', options=['Tak', 'Nie'], name='Python'),
        radio('Java', options=['Tak', 'Nie'], name='Java')
    ])
    output('aaa')
    put_text(dane)


if __name__ == '__main__':
    podajpracownika()
