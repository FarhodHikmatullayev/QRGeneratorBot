from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.generator_keyboard import generate_qr_code_default_markup
from loader import dp, db, bot


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        full_name = message.from_user.full_name
        username = message.from_user.username
        user = await db.create_user(
            username=username,
            full_name=full_name,
            telegram_id=user_telegram_id,
        )
    else:
        user = users[0]
    await message.reply(text="👋 Salom, botimizga xush kelibsiz!")
    user_role = user['role']
    if user_role == 'admin':
        await message.answer(text="📷 QR codeni skanerlash uchun uning rasmini jo'nating",
                             reply_markup=generate_qr_code_default_markup)
    elif user_role == 'cashier':
        await message.answer(text="📷 QR codeni skanerlash uchun uning rasmini jo'nating")
    else:
        await message.answer(text="🚫 Kechirasiz, sizda hali botdan foydalanish uchun ruxsat mavjud emas!")