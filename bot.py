import asyncio, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
PDF_FILE_ID = os.environ.get("PDF_FILE_ID", "")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check")]
    ])

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "👋 Hallo! Подпишись на канал и получи PDF в подарок!,",
        reply_markup=keyboard()
    )

@dp.message(F.document)
async def get_file_id(message: types.Message):
    await message.answer(f"file_id: {message.document.file_id}")

@dp.callback_query(F.data == "check")
async def check(callback: types.CallbackQuery):
    member = await bot.get_chat_member(CHANNEL_ID, callback.from_user.id)
    if member.status in ("member", "administrator", "creator"):
        await callback.message.answer("🎉 Держи твой PDF!")
        if PDF_FILE_ID:
            await callback.message.answer_document(PDF_FILE_ID)
        await callback.answer()
    else:
        await callback.answer("❌ Подпишись на канал и нажми снова.", show_alert=True)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
