"""
Napisz program, który importuje katalog z dowolnej biblioteki (np. API Biblioteki Narodowej http://data.bn.org.pl/
- przykład użycia: http://data.bn.org.pl/api/bibs.json?author=Andrzej+Sapkowski&amp;kind=ksi%C4%85%C5%BCka).
Użytkownik może podać autora i program pokaże mu, jakie książki tego autora są w zbiorach biblioteki.
Następnie daj użytkownikowi możliwość “wypożyczania” i “zwracania” książek - posiadane pozycje są składowane
w pliku zawierającym pewien identyfikujący zbiór danych, np. tytuł, autor, wydawnictwo, rok wydania (możesz też użyć
lokalnej bazy danych), w przypadku “wypożyczenia” książki są do niego dodawane, a w przypadku “zwracania” usuwane.
Propozycja rozszerzenia: W prostym przypadku lokalne “wypożyczanie” nie ma wpływu na katalog biblioteki,
czyli w teorii można wypożyczyć książkę nieskończoną liczbę razy. Zabezpiecz program w taki sposób, aby podczas
pobierania danych rozpoznawał też pozycje “wypożyczone” lokalnie i nie pokazywał ich już jako wyniki wyszukiwania.
"""

import sqlite3
import time

import requests


def create_books_table():
    """Creates books database, run it once"""
    with sqlite3.connect('books.db') as conn:
        conn.cursor().execute("""CREATE TABLE books (
                            author text,
                            title text,
                            publication_year text,
                            publisher text
                            )""")


class Book:
    def __init__(self, author, title, year, publisher):
        self._author = author
        self._title = title
        self._year = year
        self._publisher = publisher

    def __str__(self):
        return f'Author: {self._author}\nTitle: {self._title}\nPublication year: {self._year}\nPublisher: {self._publisher}\n'

    def borrow_book(self):
        """Saves 'borrowed' book in the database"""
        with sqlite3.connect('books.db') as conn:
            conn.cursor().execute("INSERT INTO books VALUES (?, ?, ?, ?)", (self._author, self._title,
                                                                            self._year, self._publisher))

    def return_book(self):
        """Returns 'borrowed' book by deleting it from the database"""
        with sqlite3.connect('books.db') as conn:
            conn.cursor().execute("""DELETE FROM books WHERE author=? AND title=? AND publication_year=? 
            AND publisher=?""", (self._author, self._title, self._year, self._publisher))

    def check_if_borrowed(self):
        """Checks if the book is already in the database."""
        with sqlite3.connect('books.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM books WHERE author=? AND title=? AND publication_year=? AND publisher=?",
                  (self._author, self._title, self._year, self._publisher))
            result = c.fetchone()
        return bool(result)


class BookList:
    def __init__(self):
        self._books = []

    def __iter__(self):
        return iter(self._books)

    def is_empty(self):
        return self._books == []

    def add_book(self, book):
        self._books.append(book)

    def add_book_data(self, books):
        """Adds book data got from api"""
        for i, book in enumerate(books):
            if books[i]['kind'] != 'książka':
                continue
            author = books[i]['author']
            title = books[i]['title']
            year = books[i]['publicationYear']
            publisher = books[i]['publisher']
            b = Book(author, title, year, publisher)
            if not b.check_if_borrowed():
                self._books.append(b)

    def find_books_from_api(self, author):
        """Finds books of the requested author in the api"""
        url = 'http://data.bn.org.pl/api/bibs.json?limit=50'
        response = requests.get(url, params={"author": author})
        books = response.json()['bibs']
        next_page = response.json().get('nextPage', None)
        self.add_book_data(books)
        while next_page:
            response = requests.get(next_page)
            books = response.json()['bibs']
            next_page = response.json().get('nextPage', None)
            self.add_book_data(books)


def make_list_of_borrowed_books():
    """Gets data from database and puts it into Booklist object"""
    with sqlite3.connect('books.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        borrowed = c.fetchall()
        borrowed_books = BookList()
        for book in borrowed:
            b = Book(book[0], book[1], book[2], book[3])
            borrowed_books.add_book(b)
        return borrowed_books


def main():
    # create_books_table()  # Run this once to create the table

    author = input('Type the author to find his books or press "q" to skip:\n')
    if author != 'q':
        try:
            booklist = BookList()
            booklist.find_books_from_api(author)
            print('Press "y" if you want to borrow the found book, "n" if not and "q" to quit.')
            for book in booklist:
                print(book)
                answer = input()
                if answer == 'y':
                    book.borrow_book()
                elif answer == 'q':
                    break
                else:
                    continue
        except:
            print('There was a problem in finding books.')

    time.sleep(1)
    books = make_list_of_borrowed_books()
    if not books.is_empty():
        print('You borrowed following books: (Press "r" if you want to return the book, "n" if not and "q" to quit):')
        for book in books:
            print(book)
            answer = input()
            if answer == 'r':
                book.return_book()
            elif answer == 'q':
                break
            else:
                continue

if __name__ == "__main__":
    main()
