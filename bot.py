import os
import requests
import smtplib
from email.message import EmailMessage

# =====================================
# GITHUB SECRETS
# =====================================

API_KEY = os.environ["OPENWEATHER_API_KEY"]

CITY = os.environ["CITY"]

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]

APP_PASSWORD = os.environ["APP_PASSWORD"]

RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]

# =====================================
# FETCH WEATHER DATA
# =====================================

url = (
    "https://api.openweathermap.org/data/2.5/forecast"
    f"?q={CITY}"
    f"&appid={API_KEY}"
    "&units=metric"
)

response = requests.get(url, timeout=20)

response.raise_for_status()

data = response.json()

forecast = data["list"][0]

temperature = forecast["main"]["temp"]

weather_condition = forecast["weather"][0]["main"]

print(f"City: {CITY}")
print(f"Temperature: {temperature}°C")
print(f"Condition: {weather_condition}")

# =====================================
# CHECK ALERT CONDITIONS
# =====================================

alert_needed = False

alert_message = []

if temperature > 35:
    alert_needed = True
    alert_message.append(
        f"🔥 High Temperature Alert!\nCurrent Temperature: {temperature}°C"
    )

if weather_condition.lower() == "rain":
    alert_needed = True
    alert_message.append(
        f"🌧 Rain Alert!\nRain is predicted in {CITY}"
    )

# =====================================
# SEND EMAIL
# =====================================

if alert_needed:

    message = EmailMessage()

    message["Subject"] = f"Weather Alert - {CITY}"

    message["From"] = EMAIL_ADDRESS

    message["To"] = RECEIVER_EMAIL

    message.set_content("\n\n".join(alert_message))

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            EMAIL_ADDRESS,
            APP_PASSWORD
        )

        smtp.send_message(message)

    print("Alert email sent successfully.")

else:

    print("No alert conditions detected.")
