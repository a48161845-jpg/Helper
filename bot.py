import json
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command


TOKEN = os.getenv("BOT_TOKEN") or "ТВОЙ_ТОКЕН"


bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Отправь JSON файл.\n"
        "Я сделаю SQL для PostgreSQL таблицы bot_kv."
    )


@dp.message(lambda m: m.document and m.document.file_name.endswith(".json"))
async def convert(message: Message):

    tg_file = await bot.get_file(
        message.document.file_id
    )

    await bot.download_file(
        tg_file.file_path,
        "data.json"
    )


    with open(
        "data.json",
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)


    sql = []

    sql.append(
        "TRUNCATE TABLE bot_kv;"
    )


    for key, value in data.items():

        json_value = json.dumps(
            value,
            ensure_ascii=False
        )

        # экранирование кавычек
        json_value = json_value.replace(
            "'",
            "''"
        )

        key = key.replace(
            "'",
            "''"
        )


        sql.append(
            f"""
INSERT INTO bot_kv (key, value)
VALUES ('{key}', '{json_value}'::jsonb);
""".strip()
        )


    with open(
        "bot_kv_import.sql",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(
            "\n\n".join(sql)
        )


    await message.answer_document(
        FSInputFile(
            "bot_kv_import.sql"
        ),
        caption="Готово ✅ Импортируй этот SQL в PostgreSQL"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
