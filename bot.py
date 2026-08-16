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

    rose = next(
        gift for gift in gifts.gifts
        if gift.id == "Rose"
    )

    await bot.send_gift(
        user_id=USER_ID,
        gift_id=rose.id
    )

    await bot.session.close()

asyncio.run(main())
