from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = "735805a16a582895f978089fb0b4a4d5"

@app.route("/")
def home():
    return "Weather Forecast App is Running!"

@app.route("/weather/<city>")
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return jsonify({
            "error": "Failed to fetch weather data",
            "details": response.json()
        }), 400

    data = response.json()

    return jsonify({
        "city": city,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
