from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "24b2faf291d14dc3a3a33107252907"  # ใส่ API Key ของคุณ

def get_weather_and_airquality(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=2&aqi=yes&alerts=no"
    response = requests.get(url)
    if response.status_code != 200:
        return None, f"เกิดข้อผิดพลาดจาก API (status code: {response.status_code})"
    data = response.json()
    if "error" in data:
        return None, data['error']['message']
    return data, None

def interpret_aqi(aqi):
    aqi_texts = {
        1: "ดี (Good)",
        2: "ปานกลาง (Moderate)",
        3: "ไม่ดีต่อสุขภาพสำหรับกลุ่มเสี่ยง (Unhealthy for Sensitive Groups)",
        4: "ไม่ดี (Unhealthy)",
        5: "ไม่ดีมาก (Very Unhealthy)",
        6: "อันตราย (Hazardous)"
    }
    return aqi_texts.get(aqi, "ไม่ทราบ")

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            data, error = get_weather_and_airquality(city)
            if data:
                current = data['current']
                air_quality = current.get('air_quality', {})
                pm25 = air_quality.get('pm2_5')
                aqi_us = air_quality.get('us-epa-index')
                aqi_desc = interpret_aqi(aqi_us)

                weather_data = {
                    "location": data['location']['name'],
                    "condition": current['condition']['text'],
                    "icon": current['condition']['icon'],  # เพิ่มบรรทัดนี้
                    "temp_c": current['temp_c'],
                    "humidity": current['humidity'],
                    "wind_kph": current['wind_kph'],
                    "pm25": pm25,
                    "aqi_desc": aqi_desc,
                    "localtime": data['location']['localtime'],
                }

                # ดึงข้อมูลพยากรณ์วันพรุ่งนี้
                if "forecast" in data and "forecastday" in data["forecast"] and len(data["forecast"]["forecastday"]) > 1:
                    tomorrow = data["forecast"]["forecastday"][1]
                    forecast_data = {
                        "date": tomorrow["date"],
                        "condition": tomorrow["day"]["condition"]["text"],
                        "icon": tomorrow["day"]["condition"]["icon"],
                        "max_temp": tomorrow["day"]["maxtemp_c"],
                        "min_temp": tomorrow["day"]["mintemp_c"],
                        "avg_humidity": tomorrow["day"]["avghumidity"],
                        "max_wind": tomorrow["day"]["maxwind_kph"],
                        "chance_of_rain": tomorrow["day"].get("daily_chance_of_rain", None),
                    }
        else:
            error = "กรุณากรอกชื่อเมือง"

    return render_template("index.html", weather=weather_data, forecast=forecast_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
