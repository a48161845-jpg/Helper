import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Отправь мне JSON файл, я сделаю SQL для PostgreSQL bot_kv"
    )


@dp.message(lambda m: m.document and m.document.file_name.endswith(".json"))
async def convert_json(message: types.Message):

    file = await bot.get_file(message.document.file_id)

    await bot.download_file(
        file.file_path,
        "input.json"
    )

    with open("input.json", "r", encoding="utf-8") as f:
        data = json.load(f)


    sql = []

    sql.append("-- Импорт bot_kv\n")

    for key, value in data.items():

        # нормальный JSON вместо [object Object]
        if isinstance(value, (dict, list)):
            value = json.dumps(
                value,
                ensure_ascii=False
            )
        else:
            value = str(value)


        value = value.replace("'", "''")

        sql.append(
            f"INSERT INTO bot_kv (key, value) VALUES "
            f"('{key}', '{value}');"
        )


    with open(
        "bot_kv_import.sql",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("\n".join(sql))


    await message.answer_document(
        FSInputFile("bot_kv_import.sql"),
        caption="Готово ✅ SQL для Adminer PostgreSQL"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
