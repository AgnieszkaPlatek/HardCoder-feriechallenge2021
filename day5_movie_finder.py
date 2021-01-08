"""
Przy wykorzystaniu API (np. IMDB) wyszukaj wszystkie części filmu zadanego w wyszukiwaniu
(np. Rambo, Scary Movie, Shrek). Można przyjąć założenie, że wszystkie filmy “z serii” muszą zawierać szukany ciąg
- czasem zdarzają się błędne wyniki wyszukiwania z baz, można je spróbować odfiltrować. Wyświetl dla każdego podstawowe
informacje np. rok, długość, ocena, spis aktorów (pierwszych 5 z listy).
Przykładowe API do wykorzystania:
https://rapidapi.com/apidojo/api/imdb8/endpoints - do wyszukania filmów z daną nazwą (do odfiltrowania można użyć
warunku, że dany rekord posiada nazwę i rok wydania)
https://rapidapi.com/.../imdb-internet-movie-database... - pobranie szczegółów o danym filmie.
"""


import os

import requests


def find_movies(title):
    """
    Finds in rapid api series of movies with a given title and makes a list of its ids.
    :param title: string
    :return: list of strings
    """
    movies_ids = []
    url = "https://imdb8.p.rapidapi.com/title/auto-complete"

    headers = {
        'x-rapidapi-key': os.environ.get('R_API_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers, params={"q": title})

    for item in r.json()['d']:
        movies_ids.append(item['id'])

    return movies_ids


def print_movie_info(movie_id):
    """
    Finds in rapid api information about the movie with a given id and prints it.
    :param movie_id: string
    :return: None
    """
    url = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{movie_id}"

    headers = {
        'x-rapidapi-key': os.environ.get('R_API_KEY'),
        'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers)
    movie = r.json()
    if movie['year'] == '' or movie['rating_votes'] == '':
        return
    if len(movie['length']) < 5:
        return
    print(f"Movie: {movie['title']}\nYear of production: {movie['year']}\nLength: {movie['length']}\nRating: {movie['rating']}")
    actors = [actor['actor'] for actor in movie['cast']][:5]
    print(f'Main actors: {", ".join(actors)}\n')


def main():
    movies_ids = find_movies(input("Type the title of the movie:\n"))
    for id in movies_ids:
        print_movie_info(id)


if __name__ == "__main__":
    main()
