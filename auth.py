import asyncio
from telethon import TelegramClient

api_id = 32696962
api_hash = "d6f6107cece05ae0e40f6f9c16a72d07"

client = TelegramClient("session", api_id, api_hash)

async def main():
    await client.start()
    print("Авторизация прошла успешно!")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

