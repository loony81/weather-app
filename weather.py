import requests
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

conditions = {
 'broken clouds': 'plural',
 'clear sky': 'singular',
 'drizzle': 'singular',
 'drizzle rain': 'singular',
 'dust': 'singular',
 'extreme rain': 'singular',
 'few clouds': 'plural',
 'fog': 'singular',
 'freezing rain': 'singular',
 'haze': 'singular',
 'heavy intensity drizzle': 'singular',
 'heavy intensity drizzle rain': 'singular',
 'heavy intensity rain': 'singular',
 'heavy intensity shower rain': 'singular',
 'heavy shower rain and drizzle': 'singular',
 'heavy shower snow': 'singular',
 'heavy snow': 'singular',
 'heavy thunderstorm': 'singular',
 'light intensity drizzle rain': 'singular',
 'light intensity shower rain': 'singular',
 'light rain and snow': 'singular',
 'light shower sleet': 'singular',
 'light shower snow': 'singular',
 'light thunderstorm': 'singular',
 'mist': 'singular',
 'moderate rain': 'singular',
 'overcast clouds': 'plural',
 'ragged shower rain': 'singular',
 'ragged thunderstorm': 'singular',
 'rain': 'singular',
 'rain and snow': 'singular',
 'sand': 'singular',
 'sand/dust whirls': 'plural',
 'scattered clouds': 'plural',
 'shower drizzle': 'singular',
 'shower rain': 'singular',
 'shower rain and drizzle': 'singular',
 'shower sleet': 'singular',
 'shower snow': 'singular',
 'sleet': 'singular',
 'smoke': 'singular',
 'snow': 'singular',
 'squalls': 'plural',
 'thunderstorm': 'singular',
 'thunderstorm with drizzle': 'singular',
 'thunderstorm with heavy drizzle': 'singular',
 'thunderstorm with heavy rain': 'singular',
 'thunderstorm with light drizzle': 'singular',
 'thunderstorm with rain': 'singular',
 'tornado': 'singular',
 'very heavy rain': 'singular',
 'volcanic ash': 'singular'
}

# this function composes correct sentences based on whether the condition has singular or plural meaning
def compose_description(condition):
    singular_or_plural = conditions.get(condition, 'singular')
    return f'There are {condition}' if singular_or_plural == 'plural' else f'There is {condition}'

# this function converts degrees into compass directions
def degrees_to_compass(degrees):
    directions = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest", "North"]
    # Normalize the degrees to be within 0-360
    degrees = degrees % 360
    # Calculate the index in the directions list
    index = int((degrees + 22.5) / 45)
    return directions[index]


# this function allows to determine the city by the ip address of a user
def get_city_by_ip():
    return requests.get('https://freeipapi.com/api/json').json()['cityName']

# strip the city name of all non-alphabetic characters
def clean_city(city):
    bad_chars = '.,:;@!#?/"\&%$*()_-+=<>0123456789'
    city = city.strip().lstrip(bad_chars).rstrip(bad_chars)
    if not city.replace(' ', '').isalpha():
        raise ValueError('Please provide a valid location')
    return city

def get_current_weather(city):
    city = clean_city(city)
    request_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv("API_KEY")}&units=metric'
    try:
        weather_data = requests.get(request_url).json()
    except (requests.ConnectionError, requests.ConnectTimeout, requests.RequestException):
        raise ConnectionError('Network error')
    if weather_data['cod'] != 200:
        raise ValueError('City not found')
    return weather_data


if __name__ == '__main__':
    print('***Get Current Weather Conditions***\n')
    city = input('Please enter a city name: ')
    try:
        weather_data = get_current_weather(city)
        print(f'{compose_description(weather_data["weather"][0]["description"])} currently in {city}.')
        print(f'The temperature is: {weather_data["main"]["temp"]}°C, but it feels like {weather_data["main"]["feels_like"]}°C')
        print(f'The humidity is {weather_data["main"]["humidity"]}% and the wind speed is {weather_data["wind"]["speed"]} m/s coming from the {degrees_to_compass(weather_data["wind"]["deg"])}.')
    except (ValueError, ConnectionError) as e:
        print(e)