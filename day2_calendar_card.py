"""
Napisz program, który po uruchomieniu wyświetla w czytelnej formie aktualną datę, godzinę, dzień tygodnia i
pogodę/temperaturę/ciśnienie w zadanym mieście (wykorzystaj np.
https://rapidapi.com/commu.../api/open-weather-map/endpoints - pamiętaj o poprawnym przeliczeniu jednostek
np. temperatura z kelwinów na stopnie) oraz losowy cytat (np. https://type.fit/api/quotes ).
Wykorzystaj requests i datetime.
Propozycja rozszerzenia: Wyświetl również bieżący czas dla miast w różnych strefach czasowych
(np. Pekin, Sydney, Waszyngton, Londyn) - wykorzystaj np. pytz: https://pypi.org/project/pytz/
oraz wyświetl listę osób obchodzących imieniny (poszukaj otwartej bazy danych lub wykorzystaj prosty web scrapping
np. z wykorzystaniem: https://imienniczek.pl/widget/js ).
"""


import os
import random
from datetime import datetime, timedelta

import requests
from requests_html import HTMLSession


def pick_quote():
    """
    Picks a random quote from 'https://type.fit/api/quotes'.
    :return: string
    """
    r = requests.get('https://type.fit/api/quotes')
    quotes = r.json()
    quote = random.choice(quotes)
    text = quote['text']
    author = quote['author'] if quote['author'] is not None else 'author unknown'
    return f'"{text}" by {author}'


def check_weather_and_timezone(city):
    """
    Checks weather and timezone for a given city.
    :param city: string
    :return: dictionary of weather, temperature, pressure and timezone and their values for a given city
    """
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    headers = {
        'x-rapidapi-key': os.environ.get('WEATHER_API_KEY'),
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers, params={"q": city})
    weather = r.json()
    weather_description = weather['weather'][0]['description']
    pressure = str(weather['main']['pressure']) + ' hPa'
    temperature = str(round(weather['main']['temp'] - 273.15, 1)) + u'\N{DEGREE SIGN}' + 'C'
    timezone = weather['timezone']
    weather_data = {'weather_description': weather_description, 'pressure': pressure, 'temperature': temperature,
                    'timezone': timezone}
    return weather_data


def check_time_and_date(difference):
    """
    Checks time and date now for a given timezone.
    :param city: integer of seconds, difference from the utc time
    :return: dictionary of date, time and day of the week and its values for a given timezone
    """
    dt_utc_now = datetime.utcnow()
    timezone = timedelta(seconds=difference)
    dt_now = dt_utc_now + timezone
    time = dt_now.time().isoformat()[:8]
    date = dt_now.strftime('%d.%m.%Y')
    weekday = dt_now.strftime('%A')
    time_and_date = {'time': time, 'date': date, 'weekday': weekday}
    return time_and_date

def check_time_other_cities(city):
    """
    Checks time in other cities
    :param city: string
    :return: None
    """
    session = HTMLSession()
    r = session.get('https://textlists.info/geography/countries-and-capitals-of-the-world/')
    cities = r.html.find('p')[2].text
    cities = cities.split('\n')[1:]
    cities = [x.split(' — ')[1] for x in cities]
    picked_cities = random.sample(cities, 5)
    for c in picked_cities:
        if c == city:
            continue
        try:
            tz = check_weather_and_timezone(c)['timezone']
            tdata = check_time_and_date(tz)
            print(f'{c} - there is {tdata["time"]}, {tdata["date"]}.')
        except:
            continue


def check_name_day():
    """
    Checks who has a name day today
    :return: list of strings representing names
    """
    session = HTMLSession()
    r = session.get('https://imienniczek.pl/widget/js?fbclid=IwAR0lCMeLzNm4ckAVrg_JGZQ0LCltS1STq_6dcYYOAa50PfxKdTYybin63Ws')
    names = r.html.find('.box_tab')[1]
    names = names.text.split('\n')
    if len(names) > 1:
        names = ', '.join(names[:-1]) + ' and ' + names[-1]
    return names


def main():
    city = input("Type a city:\n")
    weather_and_tz = check_weather_and_timezone(city)
    tdata = check_time_and_date(weather_and_tz["timezone"])
    print(f'\nTime in {city} is {tdata["time"]}, date is {tdata["date"]} and there is {tdata["weekday"]}.\n')
    print(f'Today in {city} there is {weather_and_tz["weather_description"]}.')
    print(f'The temperature is {weather_and_tz["temperature"]} and the pressure is {weather_and_tz["pressure"]}.\n')
    print(f'The quote of the day is: {pick_quote()}\n')
    print(f'Today is a name day of: {check_name_day()}.\n')
    print('In other cities:')
    check_time_other_cities(city)


if __name__ == "__main__":
    main()
