"""
В данном скрипте представлен другой скрипт, который был взят с открытого источника
https://github.com/karvozavr/weather-bot
"""

import datetime
from main import bot, dp
from aiogram import types
import os
from dotenv import load_dotenv
from bot_messages import get_message
from advice_service import get_advice
from weather_service import WeatherServiceException, WeatherInfo, get_weather_for_city
from keywords import *

WEATHER_RETRIEVAL_FAILED_MESSAGE = get_message('weather_for_location_retrieval_failed')

load_dotenv()
admin_id = os.getenv("admin_id")


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен!\n")


@dp.message_handler(commands=["start", "help"])
async def start_help_commands(message: types.Message):
    await message.answer(f"<b>Что бот умеет?</b>\n\n"
                         f"Показывает текущую дату, текущее время и погоду!\n"
                         f"Просто попросите его об этом!\n\n"
                         f"Для запроса погоды введи - Какая погода в городе Москва, либо любой другой город!\n\n"
                         f"Введи /start или /help для повторного отображения данного сообщения!")


@dp.message_handler()
async def today_date_and_time(message: types.Message):
    result = message.text.lower()
    times = datetime.datetime.now()
    s = [k for k in dictionary if result in k]
    string = "".join(s)
    if string in dictionary.keys():
        await message.answer(dictionary.get(string))
    if "сколько" in result and "сейчас" in result and "времени" in result or "текущее" in result and "время" in result:
        await message.answer(times.strftime("%H:%M:%S"))
    if "текущая" in result and "дата" in result:
        await message.answer(times.strftime("%d-%m-%Y"))
    if "текущую" in result and "дату" in result and "время" in result:
        await message.answer(times.strftime("%d.%m.%Y %H:%M:%S"))
    if 'погода' in result and 'городе' in result:
        res = result[-1:]
        city = ''.join(res)
        try:
            weather: WeatherInfo = await get_weather_for_city(city)
        except WeatherServiceException:
            await message.reply(WEATHER_RETRIEVAL_FAILED_MESSAGE)
            return

        response = get_message('weather_in_city_message') \
            .format(city, weather.status, weather.temperature) + '\n\n' + \
            get_advice(weather)

        await message.answer(response)

