import asyncio
import logging
import os
from datetime import datetime

import aiohttp
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from utils import (
    currency_names, SUBSCRIBED, UNSUBSCRIBED,
    HISTORY_BUTTON, CURRENCY_RATE_BUTTON, SUBSCRIBED_BUTTON,
    UNSUBSCRIBED_BUTTON, SELECT_ACTION, DJANGO_BASE_URL, format_message
)

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

TOKEN = os.getenv('TELEGRAM_TOKEN')


async def send_button_press_to_django(data):
    """Отправка информации о нажатии кнопки."""
    async with aiohttp.ClientSession() as session:
        await session.post(DJANGO_BASE_URL + f'users/{data["id"]}/messages/', json=data)


async def get_message_text(title: str):
    """Получение текста сообщения."""
    async with aiohttp.ClientSession() as session:
        async with session.get(DJANGO_BASE_URL + f'bot-texts/?search={title}') as response:
            text = (await response.json())[0]['text']
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка приветственного сообщения."""
    user = update.effective_user

    message_info = {
        'id': user.id,
        'username': user.username or '',
        'date': datetime.now().isoformat(),
        'text': '/start'
    }
    await send_button_press_to_django(message_info)

    is_subscribed = await check_subscription(user.id)

    welcome_text = await get_message_text('welcome')

    await update.message.reply_text(
        f'{welcome_text}',
        reply_markup=main_menu_keyboard(is_subscribed),
    )


def main_menu_keyboard(is_subscribed):
    """Клавиатура основных команд."""
    subscription_button_text = UNSUBSCRIBED_BUTTON if is_subscribed else SUBSCRIBED_BUTTON

    keyboard = [
        [KeyboardButton(CURRENCY_RATE_BUTTON)],
        [KeyboardButton(subscription_button_text)],
        [KeyboardButton(HISTORY_BUTTON)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик сообщений."""
    user = update.effective_user
    user_id = user.id
    username = user.username or ''
    text = update.message.text
    timestamp = datetime.now().isoformat()

    message_info = {
        'id': user_id,
        'username': username,
        'date': timestamp,
        'text': text
    }
    await send_button_press_to_django(message_info)
    is_subscribed = await check_subscription(user_id)

    if text == CURRENCY_RATE_BUTTON:
        currency_rates = await get_currency_rates()
        await update.message.reply_text(currency_rates, reply_markup=main_menu_keyboard(is_subscribed))

    elif text == SUBSCRIBED_BUTTON or text == UNSUBSCRIBED_BUTTON:
        await update_subscription(user_id)
        new_status = await check_subscription(user_id)
        response_text = (SUBSCRIBED if new_status else UNSUBSCRIBED)
        await update.message.reply_text(response_text, reply_markup=main_menu_keyboard(new_status))

    elif text == HISTORY_BUTTON:
        messages = await get_user_messages(user_id)
        await update.message.reply_text(messages, reply_markup=main_menu_keyboard(is_subscribed))

    else:
        await update.message.reply_text(SELECT_ACTION, reply_markup=main_menu_keyboard(is_subscribed))


async def get_currency_rates():
    """Получение актуального курса."""
    async with aiohttp.ClientSession() as session:
        async with session.get(DJANGO_BASE_URL + 'сurrency-rate/') as response:
            currency_data = await response.json()

    currency_text = await get_message_text('currency')
    exchange_text = await get_message_text('basic_exchange_rates')
    exchange_list = exchange_text.split()

    formatted_rates = currency_text + '\n' + '\n'.join(
        [f"{currency_names[currency['code']]} {currency['code']} : {currency['rate']}"
         for currency in currency_data if currency['code'] in exchange_list]
    )
    return formatted_rates


async def check_subscription(user_id):
    """Проверка подписки пользователя."""
    async with aiohttp.ClientSession() as session:
        async with session.get(DJANGO_BASE_URL + f'users/{user_id}/') as response:
            user_data = await response.json()
            return user_data['signed']


async def update_subscription(user_id):
    """Обновление статуса подписки пользователя."""
    is_subscribed = await check_subscription(user_id)
    new_subscription_status = not is_subscribed

    async with aiohttp.ClientSession() as session:
        await session.patch(DJANGO_BASE_URL + f'users/{user_id}/', json={'signed': new_subscription_status})


async def get_user_messages(user_id):
    """Получение истории сообщений пользователя."""
    async with aiohttp.ClientSession() as session:
        async with session.get(DJANGO_BASE_URL + f'users/{user_id}/messages/?limit=50') as response:
            messages_data = await response.json()

    messages_text = await get_message_text('requests_list')

    message_list = [format_message(message) for message in messages_data['results']]
    formatted_messages = messages_text + "\n" + "\n".join(message_list)

    return formatted_messages


async def send_hourly_currency_rates(bot):
    """Отправление курса валют подписанным пользователям каждый час."""
    while True:
        subscribers = await get_subscribers()
        currency_rates = await get_currency_rates()

        for user_id in subscribers:
            await bot.send_message(chat_id=user_id, text=currency_rates)
        await asyncio.sleep(60)


async def get_subscribers():
    """Получение списка пользователей с подпиской."""
    async with aiohttp.ClientSession() as session:
        async with session.get(DJANGO_BASE_URL + 'users/') as response:
            users = await response.json()
            return [user['id'] for user in users if user['signed']]


def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(f'{TOKEN}').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    loop = asyncio.get_event_loop()
    loop.create_task(send_hourly_currency_rates(application.bot))

    application.run_polling()


if __name__ == '__main__':
    main()
