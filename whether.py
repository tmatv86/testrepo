import requests
import os

WAPI_KEY = os.getenv('WAPI_KEY')
print(WAPI_KEY)
def get_whether(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WAPI_KEY}'

    print('Whether in the city: ', city)
    response = requests.get(url)

    print(response.json())

    if response.json()['cod'] != 401:
        reply = response.json()
        temp = reply['main']['temp']
        desc = reply['weather'][0]['description']
        return f'Temperature in {city}: {temp} K\n' + f'Description: {desc}'

    else:
        return f"Error fetching whether data: {response.json()['message']}"

def f_g_link(address):
    return requests.get('https://nominatim.openstreetmap.org/search', params={'q' : address}).url


