from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db


@dp.message_handler(text="🛠️ Generate QR", state="*")
async def generate_qr_code(message: types.Message, state: FSMContext):
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
    user_role = user['role']
    if user_role != 'admin':
        await message.reply(text="🚫 Sizda bu buyruqdan foydalanish uchun ruxsat mavjud emas")
        return
    else:
        print('generate funksiyasi ishlayapti')
        # qr_code = await db.create_qr_code(
        #     information=,
        # )