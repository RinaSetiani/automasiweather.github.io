from flask import Flask, render_template, request
import requests

app = Flask(__name__)

class Weather:
    def __init__(self, temp, description, min_temp, max_temp, icon):
        self.temp = temp
        self.description = description
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.icon = icon
    
    @classmethod
    def from_json(cls, json_data):
        temp = json_data['main']['temp']
        description = json_data['weather'][0]['description']
        min_temp = json_data['main']['temp_min']
        max_temp = json_data['main']['temp_max']
        icon = json_data['weather'][0]['icon']
        return cls(temp, description, min_temp, max_temp, icon)

class City:
    def __init__(self, name):
        self.name = name
    
    def get_weather(self):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=18af9bcb359d4192394b3a3b8289423e'
        response = requests.get(url.format(self.name)).json()
        return Weather.from_json(response)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['name']
        city = City(city_name)
        weather = city.get_weather()
        return render_template('index.html', temp=weather.temp, weather=weather.description, min_temp=weather.min_temp, max_temp=weather.max_temp, icon=weather.icon, city_name=city.name)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
