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
