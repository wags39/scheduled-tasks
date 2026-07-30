import requests
import smtplib
import os
#-----------------------RAIN ALERT-------------------------------------#

WEATHER_API_KEY = os.environ.get("WEATHER_KEY")
OWM = "https://api.openweathermap.org/data/2.5/forecast"
weather_params = {
    "lat": 30.956190,
    "lon":-87.382393,
    "appid": WEATHER_API_KEY,
    "cnt": 4
}

GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
GMAIL_APP = os.environ.get("GMAIL_APP")
GMAIL_SMTP = "smtp.gmail.com"
MY_EMAIL = "rwagner6282@yahoo.com"

response = requests.get(url=OWM, params= weather_params)
response.raise_for_status()
weather_data = response.json()

condition_name = ""
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True
        condition_name = hour_data["weather"][0]["description"]

if will_rain:
    with smtplib.SMTP(GMAIL_SMTP, port=587) as connection:
        connection.starttls()
        connection.login(user=GMAIL_EMAIL, password=GMAIL_APP)
        connection.sendmail(from_addr=GMAIL_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject: Weather Warning\n\nIt looks like the forecast calls for a {condition_name}. Prepare accordingly.")


