import phonenumbers
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на фактический токен вашего бота
TOKEN = '6462131020:AAE1wpqY--_K9xjrNkJVugxR68X6T3_rZMg'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def get_phone_number_info(phone_number_str):
    phone_number = phonenumbers.parse(phone_number_str, None)
    is_valid = phonenumbers.is_valid_number(phone_number)
    country_code = phonenumbers.region_code_for_number(phone_number)
    national_number = phonenumbers.national_significant_number(phone_number)
    formatted_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    number_type = phonenumbers.number_type(phone_number)
    local_format = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
    international_format = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    geographical_area = phonenumbers.length_of_geographical_area_code(phone_number)

    return {
        "is_valid": is_valid,
        "country_code": country_code,
        "national_number": national_number,
        "formatted_number": formatted_number,
        "number_type": number_type,
        "local_format": local_format,
        "international_format": international_format,
        "geographical_area": geographical_area
    }

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для анализа телефонных номеров. Просто отправь мне номер телефона, и я выведу информацию о нем.")

@dp.message_handler(regexp=r'^\+?\d+$')
async def handle_phone_number(message: types.Message):
    phone_number_str = message.text
    phone_info = get_phone_number_info(phone_number_str)

    response_text = f"Информация о номере   {phone_number_str}:\n"
    response_text += f"Действителен:   {phone_info['is_valid']}\n"
    response_text += f"Код страны:   {phone_info['country_code']}\n"
    response_text += f"Национальный номер:   {phone_info['national_number']}\n"
    response_text += f"Форматированный номер:   {phone_info['formatted_number']}\n"
    response_text += f"Тип номера:   {phone_info['number_type']}\n"
    response_text += f"Локальный формат:   {phone_info['local_format']}\n"
    response_text += f"Международный формат:   {phone_info['international_format']}\n"
    response_text += f"Географическая область:   {phone_info['geographical_area']}"

    await message.reply(response_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
