import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# set environment variables
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get["OWM_API_KEY"]
auth_token = os.environ.get["TWIL_AUTH_TOKEN"]
account_sid = os.environ.get["TWIL_ACC_SID"]

# set local LAT, LON
LAT = 38.047989
LON = -84.501640

# create dict for OpenWeather API call
weather_params = {
    'lat': LAT,
    'lon': LON,
    'appid': api_key,
    'units': 'imperial',
    'cnt': 3
}

# Test response, get weather data
response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()


def create_weather_report():
    """
    get mid-morning weather forcast, create message, return message as str.
    :return: str
    """
    message_body = ""
    reps = 0
    times = ['weather@7', 'weather@8', 'weather@9']
    for time in times:
        temp = weather_data['list'][reps]['main']['temp']
        feels_like = weather_data['list'][reps]['main']['feels_like']
        weather = weather_data['list'][reps]['weather'][0]['description']
        weather_report = f"""
        ***{time}****
        Temp: {temp}
        Feels like: {feels_like}
        Weather: {weather}
        """
        time = weather_report
        message_body += time
        reps += 1
    return message_body


def send_message(message):
    """
    send message from twilio number to specified, verified number. Prints message status.
    :param message: input message to be sent
    """
    # sets up proxy if using twilio free account, uncomment next three lines if using twilio free account
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    # client = Client(account_sid, auth_token, http_client=proxy_client)
    # comment out next line if using free account
    client = Client(account_sid, auth_token)
    # below don't forget to add + and country code before number
    text_message = client.messages.create(
        body=message,
        from_="your twilio number",
        to="number destination"
    )
    print(text_message.status)


# create and send the message
text = create_weather_report()
send_message(text)
