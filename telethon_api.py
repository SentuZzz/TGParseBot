import asyncio
import logging
from telethon import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from telethon.tl.types import InputPhoneContact

api_id = 32696962
api_hash = "d6f6107cece05ae0e40f6f9c16a72d07"

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient("session", api_id, api_hash, loop=loop)

async def _start_client_async():
    if not client.is_connected():
        await client.start()
        logging.info("Telethon клиент подключён и готов к поиску")

async def _fetch_user_by_phone_async(phone: str):
    try:
        logging.info(f"Поиск пользователя {phone} через Telethon...")

        contact = InputPhoneContact(client_id=0, phone=phone, first_name="Temp", last_name="")
        result = await client(ImportContactsRequest([contact]))

        if not result.users:
            logging.info(f"Пользователь {phone} не найден")
            return None

        user_obj = result.users[0]

        await client(DeleteContactsRequest([user_obj.id]))

        telegram_id = getattr(user_obj, 'id', None)
        username = getattr(user_obj, 'username', None)

        first_name = getattr(user_obj, 'first_name', None)
        last_name = getattr(user_obj, 'last_name', None)

        if first_name == 'Temp':
            first_name = None

        bio = getattr(user_obj, 'about', None)

        profile_photo_id = None

        logging.info(f"Получено Telethon: ID={telegram_id}, User={username}, Name={first_name} {last_name}, Bio={bio}")

        return {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "bio": bio,
            "profile_photo_id": profile_photo_id
        }

    except Exception as e:
        logging.error(f"Ошибка в fetch_user_by_phone: {e}")
        return None

def start_client_sync():
    loop.run_until_complete(_start_client_async())

def fetch_user_by_phone_sync(phone: str):
    return loop.run_until_complete(_fetch_user_by_phone_async(phone))