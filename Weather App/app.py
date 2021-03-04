import requests
import configparser
from flask import Flask, render_template ,request

app = Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('home.html')

@app.route('/results', methods = ['POST'] )
def render_results():
    zip_code = request.form['zipCode']
    api_key = get_api_key()
    data = get_weather_results(zip_code,api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    weather_description = data["weather"][0]["description"]
    location = data["name"]
    country = data["sys"]["country"]
    return render_template('results.html',  location = location, temp = temp, 
                                            weather= weather, weather_description =weather_description, 
                                            feels_like = feels_like, country = country)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code,api_key)
    r= requests.get(api_url)
    return r.json()

print(get_weather_results("08852", get_api_key()))

if __name__ == '__main__':
    app.run()



