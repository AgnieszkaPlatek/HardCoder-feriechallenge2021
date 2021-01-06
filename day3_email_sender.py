"""
Stwórz prosty program, który będzie wysyłał spersonalizowany mailing do wybranych osób. “Bazą danych” jest plik Excela
(aby było “ciekawiej” 😉 ) lub CSV, zawierający dwie kolumny z nagłówkami: “E-mail” oraz “Imię i nazwisko”
(zakładamy, że zawsze w takiej kolejności, a imię i nazwisko są oddzielone spacją). Do użytkowników należy wysłać maila
z tematem “Your image” oraz spersonalizowaną prostą treścią np. “Hi {Imię}! it’s file generated for you”. D
odatkowo w załączniku maila znajduje się plik graficzny o nazwie “{Imię}_{Nazwisko}_image.png”
(pliki są w zadanej lokalizacji). Odpowiednio zabezpiecz program (np. brakujący plik Excela, brakujące dane w Excelu,
brak pliku png) oraz zabezpiecz przed spamowaniem (np. jeden mail wysyłany co 1 sekundę).
Mogą przydać się moduły: smtplib, email, ssl, xlrd, re, os.
Propozycje rozszerzenia: dodaj opcję wysyłania maili z treścią w HTML oraz walidator poprawności maila
(np. używając wyrażeń regularnych - moduł re).
"""

import csv
import imghdr
import os
import re
import smtplib
import time
from email.message import EmailMessage

import pylightxl as xl


def is_email_valid(email):
    """
    Checks with regular expression if email format is valid, not if that email exists.
    :param email: string
    :return: boolean
    """
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')
    return bool(re.fullmatch(email_pattern, email))


def make_list_of_recipients_from_excel(xl_file):
    """
    Creates a list of recipients from a given xlsx file.
    :param xl_file: A string path to xlsx file
    :return: A list of tuples(email, name, surname)
    """
    recipients_list = []
    db = xl.readxl(fn=xl_file)
    rows = db.ws(ws='Arkusz1').rows
    next(rows)
    for row in rows:
        email = row[0]
        try:
            name, surname = row[1].split(' ')
        except (ValueError, IndexError):
            name, surname = '', ''
        recipients_list.append((email, name, surname))
    return recipients_list


def make_list_of_recipients_from_csv(csv_f):
    """
    Creates a list of recipients from a given csv file.
    :param csv_f: A string path to csv file
    :return: A list of tuples (email, name, surname)
    """
    recipients_list = []
    with open(csv_f, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for line in reader:
            email = line[0]
            try:
                name, surname = line[1].split(' ')
            except (ValueError, IndexError):
                name, surname = '', ''
            recipients_list.append((email, name, surname))
    return recipients_list


def send_email(name, surname, email_to, email_from, email_password):
    """
    Sends an HTML or plain text email with given data and attaches image if it exists, otherwise does not send it,
    only prints out the error message.
    :params name, surname, email_to, email_from, email_password: string data required to send an email
    :return: None
    """
    msg = EmailMessage()
    msg['Subject'] = 'Test Your image'
    msg['From'] = email_from
    msg['To'] = email_to
    msg.set_content(f"Hi {name}! It's file generated for you.")

    image_path = f'{name}_{surname}_image.png'

    if not os.path.exists(image_path):
        print(f'The image file for {name} {surname} is missing. Email to {email_to} has not been sent.')
        return

    with open(image_path, 'rb') as f:
        img = f.read()
        img_type = imghdr.what(f.name)
        img_name = f.name
    msg.add_attachment(img, maintype="image", subtype=img_type, filename=img_name)

    text_part, attachment_part = msg.iter_parts()
    text_part.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h2 style="color:#1C4263;">Hi {name}! It's file generated for you.</h2>
        </body>
    </html>
    """.format(**locals()), subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_from, email_password)
        smtp.send_message(msg)


def main():
    email_from = os.environ.get('EMAIL_HOST_USER')
    email_password = os.environ.get('EMAIL_HOST_PASSWORD')
    file = 'recipients.csv'
    # file = 'recipients.xlsx'
    if os.path.exists(file):
        list_of_recipients = make_list_of_recipients_from_csv(file)
        # list_of_recipients = make_list_of_recipients_from_excel(file)

        for email_to, name, surname in list_of_recipients:
            if not is_email_valid(email_to):
                print(f'The email address of {name} {surname} is invalid.')
                continue
            if name == '' or surname == '':
                print(f'There is data missing for {name} {surname} {email_to}, email could not be sent.')
                continue
            send_email(name, surname, email_to, email_from, email_password)
            time.sleep(1)
    else:
        print('Your file with data is incorrect! No emails could be sent.')


if __name__ == "__main__":
    main()
