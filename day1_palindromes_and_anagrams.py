"""
Napisz program, który prosi użytkownika o podanie dowolnego napisu. Następnie program wyświetla na ekranie
to słowo wspak (od prawej do lewej) i wyświetla komunikat czy to wyrażenie jest palindromem
(czyli czytane wspak daje do samo wyrażenie np. “ala”, “Kobyła ma mały bok”
(inne przykłady: http://www.palindromy.pl/pal_kr.php).
Podczas sprawdzania ignoruj wielkość liter oraz znaki niebędące literami.
Następnie wywołaj dowolną stronę internetową, która pokaże anagramy oraz słowa utworzone po usunięciu liter,
np. https://poocoo.pl/scrabble-slowa-z-liter/hardcoder
Propozycja rozszerzenia: samodzielnie wyszukaj anagramy i słowa utworzone po usunięciu liter z podanego słowa,
na przykład wykorzystując słownik wspomniany na stronie https://anagramy.wybornie.com/
"""

import webbrowser

from requests_html import HTMLSession


def is_palindrome(s):
    s = [x.lower() for x in list(s) if s.isalpha()]
    s = ''.join(s)
    return s == s[::-1]


def find_anagrams(w):
    session = HTMLSession()
    try:
        r = session.get('https://anagramy.wybornie.com/' + w)
    except Exception:
        print('Problems occured in looking for anagrams.')
    p = r.html.find('p')[1]
    # Excluding sentence: "Po usunięciu niektórych liter mogą powstać wyrazy:"
    words = p.text.split()[7:]
    # Excluding letters combinations
    anagrams = [word.rstrip(',') for word in words if not word.isupper()]
    return anagrams


def main():
    word = input('Type a word to check if it is a palindrome:\n')
    print(word[::-1])
    print('Your word is a palindrome!') if is_palindrome(word) else print('Sorry, your word is not a palindrome!')
    webbrowser.open('https://poocoo.pl/scrabble-slowa-z-liter/' + word)
    anagrams = find_anagrams(word)
    if anagrams:
        print('Anagrams from your word are:')
        for anagram in anagrams:
            print(anagram)


if __name__ == "__main__":
    main()
