import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from io import BytesIO
from loader import dp, db
import secrets
import string
import qrcode

from states.qrcode import CreateQRCodeState


async def generate_unique_code(length=30):
    characters = string.ascii_letters + string.digits

    unique_code = ''.join(secrets.choice(characters) for _ in range(length))
    qr_codes = await db.select_qr_codes(information=unique_code)
    while qr_codes:
        unique_code = ''.join(secrets.choice(characters) for _ in range(length))
        qr_codes = await db.select_qr_codes(information=unique_code)
    return unique_code


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
        await message.answer(text="✍️ Foydalanuvchi ism-familiyasini kiriting:")
        await CreateQRCodeState.user_name.set()


@dp.message_handler(state=CreateQRCodeState.user_name)
async def get_user_name(message: types.Message, state: FSMContext):
    user_name = message.text
    unique_code = await generate_unique_code()
    new_qr_code = await db.create_qr_code(
        information=unique_code,
        user_name=user_name
    )

    # generate QR code with information
    # data = {
    #     'unique_code': unique_code,
    #     'user_name': user_name
    # }
    # json_data = json.dumps(data)
    data = unique_code

    qr = qrcode.QRCode(
        version=1,  # QR kod versiyasi (1 dan 40 gacha)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Xato to'g'rilash darajasi
        box_size=10,  # Har bir qismning o'lchami
        border=4,  # Qoplama chegarasi
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    await message.answer_photo(photo=img_byte_arr)
    await state.finish()
