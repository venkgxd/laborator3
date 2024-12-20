from aiogram import Bot, Dispatcher, types, executor
import requests

TOKEN = "7942770267:AAHtl0tNOUYDN85clcjrokoReOSEAaVrwNQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



def get_weather():
    try:
        API_KEY = "dd4fb27f5f66ced28253c1ff77ef45b5"  # Ваш API-ключ
        URL = f"http://api.openweathermap.org/data/2.5/weather?q=Samara&units=metric&appid={API_KEY}"


        response = requests.get(URL)
        print(f"Статус ответа: {response.status_code}")  # Для отладки
        print(f"Ответ API: {response.text}")  # Для отладки


        if response.status_code != 200:
            return f"Ошибка API: {response.status_code}. Проверьте API-ключ или параметры запроса.

        data = response.json()
        if "main" in data:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"].capitalize()
            return f"Сейчас в Самаре: {temp}°C, {weather_desc}"
        elif "message" in data:
            return f"Ошибка API: {data['message']}"
        else:
            return "Не удалось получить данные о погоде. Попробуйте позже."
    except Exception as e:
        return f"Ошибка при запросе: {e}"


# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_button = types.KeyboardButton("Узнать погоду в Самаре")
    keyboard.add(weather_button)

    await message.reply(
        "Привет! Я погодный бот. Нажми на кнопку ниже, чтобы узнать погоду в Самаре или воспользуйся командой /help для подсказки.",
        reply_markup=keyboard
    )


# /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(
        "Доступные команды:\n"
        "/start - Начать общение с ботом\n"
        "/help - Вывести список команд\n"
        "Нажмите на кнопку 'Узнать погоду в Самаре' для получения информации о погоде."
    )



@dp.message_handler(lambda message: message.text == "Узнать погоду в Самаре")
async def send_weather(message: types.Message):
    weather_info = get_weather()
    await message.reply(weather_info)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
# https://t.me/weatherZVS_bot