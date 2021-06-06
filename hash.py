import mariadb
import hashlib
import os


def connect_database():
    connection = mariadb.connect(
        user='projectOneUser',
        password='VeryHardP@ssw0rd',
        host="localhost",
        port=3306,
        database="ioProjectOne"
    )
    return connection


def hash_login(password):
    salt = os.urandom(32)       # Remember this

    key = hashlib.pbkdf2_hmac(
        'sha256',       # The hash digest algorithm for HMAC
        password.encode('utf-8'),   # Convert the password to bytes
        salt,   # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    return salt, key


def login_veryfication(salt, key, password_to_check):
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password_to_check.encode('utf-8'),
        salt,
        100000
    )

    if new_key == key:
        print('Password is correct')
    else:
        print('Password is incorrect')
        raise ValueError("Wrong password")
