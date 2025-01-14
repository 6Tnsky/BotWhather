# bot.py

import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from config import TOKEN, APIKEY

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функция для получения погоды из API
def get_weather(city: str):
    url = f"http://api.weatherapi.com/v1/current.json?key={APIKEY}&q={city}&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()

        # Проверяем успешность ответа
        if "current" in data:
            temperature = data["current"]["heatindex_c"]
            return f"Температура {temperature} градусов"
        else:
            return "Город не найден"
    except Exception as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return "Ошибка при получении данных о погоде"

@dp.message_handler(commands=["start"])
async def start_command(message: Message):
       await message.reply("Введите город:")

@dp.message_handler(commands=["help"])
async def help_command(message: Message):
       await message.reply("Наберите в сообщении город на английском языке, и я покажу температуру воздуха.")

# Обработчик текстовых сообщений
@dp.message_handler()
async def send_weather(message: Message):
    city = message.text.strip()  # Получаем текст сообщения (название города)
    weather_info = get_weather(city)  # Получаем данные о погоде
    await message.reply(weather_info)  # Отправляем ответ пользователю

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)