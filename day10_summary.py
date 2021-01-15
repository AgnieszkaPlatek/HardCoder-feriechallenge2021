"""
Napisz program, który odczytuje wszystkie pliki stworzone przez Ciebie podczas #feriechallenge - przeszukuje lokalne
katalogi lub łączy się w tym celu z Githubem. Postaraj się jak najmniej hardcodować i na przykład nie podawaj listy
wszystkich plików ręcznie 🙂  Następnie wykorzystując swój sposób katalogowania programów automat
odczytuje i wyświetla takie informacje:
-> do ilu zadań z 10 napisało się kod
-> liczba linijek kodu napisanych w każdym zadaniu (bez uwzględniania pustych!) oraz sumaryczna liczba linijek
-> liczba unikalnych słów użytych we wszystkich programach oraz najczęściej występujące słowo
-> lista i liczba słów kluczowych użyta podczas całego challenge (wykorzystaj moduł keywords)
-> lista i liczba zaimportowanych modułów we wszystkich programach
"""

import keyword
import os
from collections import Counter


def read_python_files():
    """
    Reads python files from current working directory and makes required statistics.
    :return: dictionary
    """
    python_files = []
    lines_total = 0
    words_total = {}
    keywords_total = set()
    imports_total = set()
    most_common_word = ''

    for filename in os.listdir(os.getcwd()):
        if not filename.endswith('.py') or filename.startswith('day10'):
            continue
        file_data = {'filename': filename}
        with open(filename, 'r', encoding="utf8") as f:
            data = f.read()
            for char in ':,.!?\"\'[]()\\/':
                data = data.replace(char, ' ')
            lines = [line for line in data.splitlines() if line != '']
            start = 0
            for i, line in enumerate(lines):
                if "import" in line and ("import" in lines[i + 1] or lines[i + 1] == '\n'):
                    start = i
                    break
            lines = [line for line in lines[start:] if line != '\n']
            imports = {line for line in lines if "import" in line}
            words = []
            for line in lines:
                words += line.split(' ')
            words = [word.rstrip('\n') for word in words if word != '']
            word_cnt = Counter()
            for word in words:
                word_cnt[word] += 1
            keywords = {word for word in words if keyword.iskeyword(word)}
            file_data['lines'] = len(lines)
            lines_total += len(lines)
            words_total.update(word_cnt)
            keywords_total.update(keywords)
            imports_total.update(imports)
            python_files.append(file_data)

        most_common_word = max(words_total.items(), key=lambda x: x[1])


    return {'python_files': python_files, 'lines_total': lines_total, 'keywords': keywords_total,
            'imports': imports_total, 'most_common_word': most_common_word, 'num_words': len(words_total)}


def print_stats(pydata):
    """
    Prints statistic data from the dictionary.
    :param pydata: dictionary
    :return: None
    """
    print(f"""You wrote code for {len(pydata['python_files'])+1} python programming tasks out of 10 with 
{pydata['lines_total']} lines of code.\n""")
    for file in pydata['python_files']:
        print(f"In {file['filename']} you wrote {file['lines']} lines.")
    print()
    print(f"You wrote {pydata['num_words']} unique words.")
    print(f"Most common word was \"{pydata['most_common_word'][0]}\" used {pydata['most_common_word'][1]} many times.\n")
    print(f"You used {len(pydata['imports'])} imports:")
    for line in pydata['imports']:
        print(line)
    print()
    print(f"You used {len(pydata['keywords'])} keywords:")
    print(', '.join(pydata['keywords']))


def main():
    pydata = read_python_files()
    print_stats(pydata)


if __name__ == "__main__":
    main()
