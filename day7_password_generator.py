#! python3
"""
Napisz program do generowania losowych haseł o zadanej przez użytkownika długości. Hasło musi spełniać zadane warunki
np. co najmniej jedna liczba, co najmniej po jednej dużej i małej literze. Warto skorzystać z modułów string i secrets.
Propozycja rozszerzenia: Po wygenerowaniu hasła skopiuj je do schowka systemowego 🙂
"""

import secrets
import string
import sys

import pyperclip


def generate_strong_password(n=10):
    """
    Generates strong password.
    :param n: integer
    :return:
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        p = ''.join(secrets.choice(chars) for _ in range(n))
        if any(c.islower() for c in p) and any(c.isdigit() for c in p) and any(c in string.punctuation for c in p):
            break
    return p


def main():
    if sys.stdin.isatty():
        if len(sys.argv) > 1:
            password = generate_strong_password(int(sys.argv[1]))
        else:
            password = generate_strong_password()
    else:
        n = input('Type the number of at least 8 characters in your password or press "t" to let it be 10.\n')
        if n == 't':
            password = generate_strong_password()
        try:
            n = int(n)
            if n < 8:
                print('It is not possible to generate a safe password with less than 8 characters, sorry!')
                quit()
            password = generate_strong_password(n)
        except ValueError:
            print('Please try again, make sure than the number consists of digits only.')
            quit()

    print('Your password is in the clipboard!')
    pyperclip.copy(password)


if __name__ == "__main__":
    main()
