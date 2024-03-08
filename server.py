from flask import Flask, render_template, request
from weather import get_current_weather, degrees_to_compass, compose_description
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    try:
        weather_data = get_current_weather(city)
    except (ValueError, ConnectionError) as e:
        # render error.html in case of an error
        return render_template('error.html', error=e)

    return render_template(
        'weather.html',
        city=weather_data["name"],
        description=compose_description(weather_data["weather"][0]["description"]),
        temp=f'{weather_data["main"]["temp"]:.1f}',
        feels_like=f'{weather_data["main"]["feels_like"]:.1f}',
        humidity=weather_data["main"]["humidity"],
        wind_speed=weather_data["wind"]["speed"],
        wind_direction=degrees_to_compass(weather_data["wind"]["deg"])
    )



if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
