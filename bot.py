import telebot
import time
from db import get_user, save_user, is_outdated, create_table
from telethon_api import fetch_user_by_phone_sync, start_client_sync

TOKEN = "8509415173:AAE5JYgx8QyLpJIj6bcFShfDKNzQL5XY5ho"
bot = telebot.TeleBot(TOKEN)

create_table()

try:
    start_client_sync()
except Exception as e:
    print(f"⚠️ Ошибка старта Telethon (проверьте интернет/VPN): {e}")

def safe_send(chat_id, text):
    try:
        bot.send_message(chat_id, text)
    except Exception as e:
        print(f"❌ Не удалось отправить сообщение (сбой сети): {e}")

@bot.message_handler(commands=['start'])
def start(message):
    safe_send(
        message.chat.id,
        "Привет!\nОтправь номер телефона в формате +79991234567"
    )

@bot.message_handler(func=lambda m: True)
def handle_phone(message):
    phone = message.text.strip()

    safe_send(message.chat.id, "🔍 Ищу данные...")

    user_row = get_user(phone)
    if user_row and not is_outdated(user_row):
        text = (
            "Данные из базы:\n"
            f"ID: {user_row['telegram_id'] or 'NONE'}\n"
            f"Username: {user_row['username'] or 'NONE'}\n"
            f"First Name: {user_row['first_name'] or 'NONE'}\n"
            f"Last Name: {user_row['last_name'] or 'NONE'}\n"
            f"Bio: {user_row['bio'] or 'NONE'}\n"
            f"Обновлено: {user_row['updated_at']}"
        )
        safe_send(message.chat.id, text)
        return

    try:
        data = fetch_user_by_phone_sync(phone)
    except Exception as e:
        safe_send(message.chat.id, f"❌ Ошибка поиска (Telethon): {e}")
        return

    if not data:
        safe_send(message.chat.id, "❌ Пользователь не найден или нет доступа к данным.")
        return

    save_user(
        phone=phone,
        telegram_id=data.get("telegram_id"),
        username=data.get("username"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        bio=data.get("bio"),
        profile_photo_id=data.get("profile_photo_id")
    )

    text = (
        "Данные получены через Telethon:\n"
        f"ID: {data.get('telegram_id') or 'NONE'}\n"
        f"Username: {data.get('username') or 'NONE'}\n"
        f"First Name: {data.get('first_name') or 'NONE'}\n"
        f"Last Name: {data.get('last_name') or 'NONE'}\n"
        f"Bio: {data.get('bio') or 'NONE'}\n"
        f"Profile Photo ID: {data.get('profile_photo_id') or 'NONE'}"
    )
    safe_send(message.chat.id, text)

if __name__ == "__main__":
    print("Bot started...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Перезапуск... Ошибка: {e}")
            time.sleep(3)