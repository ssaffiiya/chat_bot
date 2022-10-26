import aioschedule
import asyncio

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

from config import TOKEN
from sheets import output_V, output_M

bot=Bot(token=TOKEN)
dp=Dispatcher(bot,storage=MemoryStorage())

video_materials=InlineKeyboardButton("Видео материалы", callback_data="video")
more_materials=InlineKeyboardButton("Дополнительные материалы", callback_data="more")
MENU=InlineKeyboardMarkup().add(video_materials).add(more_materials)


@dp.message_handler(commands=['start'])
async def start_command(message:types.Message):
    await message.reply("Привет!\nТы попал на обучающего чат бота по питону.\nДля того чтобы получить хорошие результаты в обучении нужно заниматься каждый день\n Скажи, в какое время ты хочешь получать уведомления с напоминание позаниматься?")

@dp.message_handler(content_types=['text'])
async  def scheduler(message: types.Message):
    await bot.send_message(message.from_user.id, f"Жди уведомления каждый день в {message.text}\n Теперь можно и позаниматься\nВыбери интересующий тебя раздел ",reply_markup=MENU)
    tim = message.text
    aioschedule.every().day.at(tim).do(bot.send_message, message.from_user.id, text="Пор позаниматься\n Выбери интересующий тебя раздел ",reply_markup=MENU)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)

@dp.callback_query_handler(text=["video"])
async def send_video_links(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    video = output_V()
    output="\n".join(video)
    await bot.send_message(callback_query.from_user.id,text=f"Видеоролики:\n{output}")

@dp.callback_query_handler(text=["more"])
async def send_video_links(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    more=output_M()
    print(more)
    output = "\n".join(more)
    await bot.send_message(callback_query.from_user.id,text=f"Дополнительные материалы:\n{output}")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

