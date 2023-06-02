import requests
import telebot
from geopy.geocoders import Nominatim


TOKEN = ''
geolocator = Nominatim(user_agent="telegram-bot")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome_message(message):
    bot.reply_to(message, "Привет! Я бот погоды. Напишите название города, чтобы узнать погоду.")


@bot.message_handler(func=lambda message: True)
def send_weather_handler(message):
    city = message.text
    location = geolocator.geocode(city)
    if location is None:
        return bot.reply_to(message, "Не удалось найти такой город. Попробуйте еще раз.")
    x = {"X-Yandex-API-Key": "00271e6a-ef16-4c6e-9fae-9d044"}
    url = f"https://api.weather.yandex.ru/v2/informers?lat={location.latitude}&lon={location.longitude}"
    response = requests.get(url, headers=x)
    if response.status_code == 200:
        answer = response.json()
        temp = answer['fact']['temp']
        feels_like = answer['fact']['feels_like']
        humidity = answer['fact']['humidity']
        wind_speed = answer['fact']['wind_speed']
        message_text = f"Погода в городе {location.address}: \nТемпература: {temp}°C (ощущается как {feels_like}°C)\n" \
                       f"Влажность: {humidity}%\nСкорость ветра: {wind_speed} м/с"
        return bot.send_message(message.chat.id, message_text)
    return bot.reply_to(message, "Ошибка при получении данных о погоде. Попробуйте позже.")


bot.polling()
