import time

import requests
from datetime import datetime
import smtplib
MY_MAIL="abc@mail.com"//Your Mail
MY_PASSWORD="1234"//Your Password



MY_LAT =76 # Your latitude
MY_LONG = 12# Your longitude

def isover():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    
     iss_latitude = float(data["iss_position"]["latitude"])
     iss_longitude = float(data["iss_position"]["longitude"])
    
    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        print("Look up")
        return True
    else:
        print("A mail will be sent")
#Your position is within +5 or -5 degrees of the ISS position.


def night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now>=sunset or time_now<=sunrise:
        print('Its night')
        return True

#If the ISS is close to my current position

# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
while True:
    time.sleep(60)
    if night() and isover():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_MAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_MAIL,
            to_addrs=MY_MAIL,
            msg="Subject:Look up/n/n The Iss is above in the sky."
        )


