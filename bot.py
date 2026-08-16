import os
import asyncio

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = 7958252339

async def main():
    bot = Bot(BOT_TOKEN)

    gifts = await bot.get_available_gifts()

    print("Доступные подарки:")

    for gift in gifts.gifts:
        print(
            f"ID: {gift.id} | "
            f"Stars: {gift.star_count}"
        )

    await bot.session.close()


asyncio.run(main())
