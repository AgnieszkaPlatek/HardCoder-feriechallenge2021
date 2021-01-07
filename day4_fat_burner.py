"""
Napisz program, który na podstawie masy [kg] i wzrostu [cm] wylicza wskaźnik BMI
(https://en.wikipedia.org/wiki/Body_mass_index) oraz informuje użytkownika, w jakim jest zakresie.
Zakresy można wpisać “z palca” (ale może nieco mądrzej niż ciągiem if-elif-else dla każdego zakresu! 😉 ) albo odczytać
z dowolnego API, np. https://rapidapi.com/navii/api/bmi-calculator . Następnie program losuje jedną z aktywności
fizycznych oraz czas jej wykonania, np. bieganie przez 30 minut. Czas nie może być dłuższy niż podany przez użytkownika
(maksymalny czas, który można poświęcić na ćwiczenia). Zadbaj o to, aby czas aktywności był jakoś uzależniony od BMI
(na przykład osoba z niedowagą nie powinna ćwiczyć mniej niż osoba o wadze normalnej - ustal pewien minimalny czas;
ale już osoba z nadwagą powinna ćwiczyć dłużej - ustal odpowiedni nieliniowy mnożnik, tak aby nie przekroczyć maksimum).
Utwórz w ten sposób plan treningowy na 7 następnych dni, wyniki zapisując do pliku .txt.
Propozycja rozszerzenia: przygotuj urozmaicony plan treningowy uwzględniający maksymalny czas wpisany przez użytkownika
 - kilka aktywności fizycznych ma wypełniać całą dzienną ilość czasu, mają zajmować jakąs ustaloną minimalną długość
 (np. 10 minut) oraz nie mogą się powtarzać jednego dnia.
"""

import math
import os
import random
from datetime import date, timedelta

import requests


def check_bmi_and_category(height, weight):
    """
    Checks BMI using rapidapi.
    :param height: integer (centimetres)
    :param weight: integer (kilogram)
    :return: float, string
    """
    url = "https://fitness-api.p.rapidapi.com/fitness"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': os.environ.get('R_API_KEY'),
        'x-rapidapi-host': "fitness-api.p.rapidapi.com"
    }

    res = requests.request("POST", url, data=f"height={height}&weight={weight}", headers=headers)
    bmi = res.json()["bodyMassIndex"]["value"]
    category = res.json()["bodyMassIndex"]["conclusion"]
    return bmi, category


def make_list_of_dates():
    """
    Creates list of dates in string format for seven days from today
    :return: list of strings
    """
    today = date.today()
    list_of_dates = [today + timedelta(days=i) for i in range(1, 8)]
    list_of_dates = [x.strftime("%d %B %Y") for x in list_of_dates]
    return list_of_dates


def pick_exercises(min_time, max_time, category, multiple):
    """
    Picks exercises tailored to the user's preferences and weight category.
    :param min_time, max_time: integers
    :param category: string
    :param multiple: boolean
    :return: list of strings
    """
    time_choices = [x for x in range(min_time, max_time + 1, 5)]
    exercise_list = ['walking', 'cycling', 'youtube training or dancing', 'scootering or rollerblading',
                     'soccer or volleyball', 'badminton or table tennis', 'strength training', 'outdoor gym']

    if category.startswith("Obese") or category.startswith("Pre-obese"):
        exercise_list = exercise_list[:] + ['nordic walking']
        time_choices = time_choices[len(time_choices)//2:]
    else:
        exercise_list = exercise_list[:] + ['running', 'tabata or rope jumping']

    exercises = random.sample(exercise_list * 2, 7)
    times = [random.sample(time_choices, 1)[0] for _ in range(7)]
    if multiple:
        for i in range(7):
            if times[i] < 50:
                continue
            else:
                new_time = math.ceil((times[i]//2 + random.choice([5, 10]))/5) * 5
                new_exercise = random.choice(exercise_list)
                while exercises[i] == new_exercise:
                    new_exercise = random.choice(exercise_list)
                times[i] = (new_time, times[i]-new_time)
                exercises[i] = (exercises[i], new_exercise)

    ex_and_time = []
    for i in range(7):
        if isinstance(times[i], int):
            ex_and_time.append(f'{exercises[i]} for {times[i]} minutes')
        else:
            ex_and_time.append(f'{exercises[i][0]} for {times[i][0]} minutes and {exercises[i][1]} for {times[i][1]} minutes')
    return ex_and_time


def make_exercise_table(exercises):
    """
    Creates exercise table and saves it in txt file.
    :param exercises: List of strings
    :return:
    """
    dates = make_list_of_dates()
    d_max = len(max(dates, key=len))
    line = d_max + len(max(exercises, key=len)) + 3
    content = '-' * line
    for i in range(7):
        content += '\n' + dates[i].ljust(d_max, ' ') + ' | ' + exercises[i] + '\n'
        content += '-' * line
    with open('exercises.txt', 'w') as f:
        f.write(content)


def main():
    height = int(input('Type your height in centimeters:\n'))
    weight = int(input('Type your weight in kilograms:\n'))
    bmi, category = check_bmi_and_category(height, weight)
    print(f'Your BMI is {bmi} and your category is "{category}"')
    if bmi < 16 or bmi > 35:
        print("You should consult your doctor first. We do not feel qualified to give you any advise :(.")
        quit()
    min_time = int(input('Type minimum time in minutes that you can dedicate to exercise, it is recommended to make it no less than 30 ;):\n'))
    max_time = int(input('Type maximum time in minutes that you can dedicate to exercise:\n'))
    multiple = input('Would you like to have sometimes suggested more than one activity per day? Type "y" for yes and "n" for no.\n')
    multiple = False if multiple == 'n' else True
    exercises = pick_exercises(min_time, max_time, category, multiple)
    make_exercise_table(exercises)
    print("Your training plan for next week is ready! Check your exercises.txt file!")


if __name__ == "__main__":
    main()
