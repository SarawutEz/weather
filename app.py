from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "24b2faf291d14dc3a3a33107252907"  # ใส่ API Key ของคุณ

def get_weather_and_airquality(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes"
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
                    "temp_c": current['temp_c'],
                    "humidity": current['humidity'],
                    "wind_kph": current['wind_kph'],
                    "pm25": pm25,
                    "aqi_desc": aqi_desc,
                }
        else:
            error = "กรุณากรอกชื่อเมือง"

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
