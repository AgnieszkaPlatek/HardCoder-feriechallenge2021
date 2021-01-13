"""
Napisz program liczący odległość liniową między dwoma dowolnymi punktami na mapie, wykorzystujący ich współrzędne
geograficzne (długość i szerokość geograficzną). Wykorzystaj dowolny algorytm,
np. https://pl.wikibooks.org/.../Astrono.../Odleg%C5%82o%C5%9Bci
Skorzystaj z API (np. https://rapidapi.com/trueway/api/trueway-geocoding), żeby obliczyć odległość pomiędzy twoim
adresem, a charakterystycznymi punktami np. Wieżą Eiffla czy Tadź Mahal.
Propozycja rozszerzenia: zamiast podawać swój adres, użyj geolokalizacji 🙂
"""

import os

import geocoder
import requests
from geopy import distance


def find_coordinates(place):
    """
    Finds coordinates of a given place.
    :param place: string
    :return: tuple of latitude and longitude
    """

    url = "https://trueway-geocoding.p.rapidapi.com/Geocode"

    headers = {
        'x-rapidapi-key': os.environ.get('R_API_KEY'),
        'x-rapidapi-host': "trueway-geocoding.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params={"address": place})
    location = response.json()['results'][0]['location']
    return location['lat'], location['lng']


def find_distance(a, b):
    """
    Finds geodesic distance between two geograpihic points, uses default WGS-84 ellipsoid.
    :param a: tuple of coordinates (latitude, longitude)
    :param b: tuple of coordinates (latitude, longitude)
    :return: float distance in kilometers
    """
    return round(distance.geodesic(a, b).kilometers, 2)


def find_my_ip_location():
    g = geocoder.ip('me')
    return tuple(g.latlng)


def main():
    point_a = 'Eiffel Tower'  # Change it as you wish
    point_b = 'Taj Mahal'  # Change it as you wish
    a = find_coordinates(point_a)
    b = find_coordinates(point_b)
    c = find_my_ip_location()  # geolocation from IP address
    print(f'Distance between {point_a} and {point_b} is {find_distance(a, b)} km.')
    print(f'Distance between me and {point_a} is {find_distance(a, c)} km.')


if __name__ == "__main__":
    main()
