from flask import Flask, render_template, request, url_for
import requests

app = Flask(__name__)
API_KEY = "9fc7a7a2964c1df2075fcad2c3bff67b"

WEATHER_BG_MAP = {
    "clear": "clear.jpeg",  # make sure file extension matches
    "rain": "rain.gif",
    "cloud": "clouds.gif",
    "snow": "snow.gif"
}

def get_background(description):
    desc = description.lower()
    for key in WEATHER_BG_MAP:
        if key in desc:
            return url_for('static', filename=f'background/{WEATHER_BG_MAP[key]}')
    return url_for('static', filename='background/default.gif')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    background_url = url_for('static', filename='background/default.gif')
    if request.method == 'POST':
        city = request.form['city'].strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            description = data['weather'][0]['description']
            weather = {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'description': description,
                'icon': data['weather'][0]['icon']
            }
            background_url = get_background(description)
        else:
            weather = {'error': 'City not found.'}
    return render_template('index.html', weather=weather, background_url=background_url)

if __name__ == '__main__':
    app.run(debug=True)
