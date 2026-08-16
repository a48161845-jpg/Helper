import os
import asyncio

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = 5721696778
ROSE_ID = "5168103777563050263"


async def main():
    bot = Bot(BOT_TOKEN)

    try:
        await bot.send_gift(
            user_id=USER_ID,
            gift_id=ROSE_ID,
            text="🌹 Роза от бота!"
        )
        print("✅ Роза отправлена!")
    finally:
        await bot.session.close()


asyncio.run(main())
