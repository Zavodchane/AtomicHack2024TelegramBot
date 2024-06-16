import asyncio
import os
from uuid import uuid4

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import (
    Message,
    InputMediaDocument,
    FSInputFile,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ultralytics import YOLOv10

from src import User, Image, Defect
from src.config import settings, BASE_DIR
from src.database import database
from src.model import utils as model_utils

global model_YOLOv10

telegram_bot = Bot(token=settings.telegram_bot.token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет!\n"
        "Я умею детектировать и классифицировать дефекты сварных швов!\n"
        "Отправь мне фото и я помогу тебе!"
    )


@dp.message(F.photo)
async def detection_and_classifier_photo(
    message: Message,
    bot: Bot,
    session: AsyncSession = database.get_scoped_session(),
):
    photo = message.photo[-1]
    photo_name: str = f"{photo.file_id}.jpg"
    await bot.download(photo, destination=os.path.join(BASE_DIR, photo_name))

    predicate_image_path, caption, csv_path = await model_utils.predicate_image(
        path=BASE_DIR,
        photo_name=photo_name,
        model=model_YOLOv10,
        session=session,
        chat_id=message.chat.id,
    )

    media: list = []
    filename = str(uuid4())
    photo = FSInputFile(predicate_image_path, filename=f"{filename}.jpeg")
    media.append(InputMediaDocument(media=photo, caption=caption))
    file = FSInputFile(csv_path, filename=f"{filename}.csv")
    media.append(InputMediaDocument(media=file))

    await bot.send_media_group(chat_id=message.chat.id, media=media)


@dp.message(Command("statistic"))
async def cmd_start(
    message: types.Message,
    bot: Bot,
    session: AsyncSession = database.get_scoped_session(),
):
    user = await session.scalar(
        select(User)
        .where(User.id == str(message.chat.id))
        .options(
            selectinload(
                User.images,
            ).options(
                selectinload(
                    Image.defects,
                )
            )
        )
    )

    date: list = []
    defect_count: list = []
    user_images: list[Image] = user.images
    for image in user_images:
        defects: list[Defect] = image.defects

        if image.created_at in date:
            index = date.index(image.created_at)
            defect_count[index] += len(defects)
        else:
            date.append(image.created_at)
            defect_count.append(len(defects))

    data = {
        "date": date,
        "defect_count": defect_count,
    }

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["date"])

    plt.figure(figsize=(10, 6))
    sns.lineplot(x="date", y="defect_count", data=df, marker="o")
    plt.title("Количество брака в день")
    plt.xlabel("Дата")
    plt.ylabel("Количество брака")
    plt.grid(True)
    plt.savefig(os.path.join(BASE_DIR, "defective_welds_over_time.png"))

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile(os.path.join(BASE_DIR, "defective_welds_over_time.png")),
    )


@dp.message()
async def main():
    global model_YOLOv10
    model_YOLOv10 = YOLOv10(os.path.join(BASE_DIR, "weights", "best.pt"))
    await dp.start_polling(telegram_bot)


if __name__ == "__main__":
    asyncio.run(main())
