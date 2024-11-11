import json
import os
import cv2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from loader import db, dp, bot


@dp.message_handler(state="*", content_types=ContentType.PHOTO)
async def scan_qr_code(message: types.Message, state: FSMContext):
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

    if user['role'] not in ['admin', 'cashier']:
        await message.reply(text="🚫 Sizda bu buyruqdan foydalanish uchun ruxsat mavjud emas")
        return

    photo_id = message.photo[-1].file_id
    photo = await bot.get_file(photo_id)
    file_path = os.path.join('yuklab olingan', f"{photo_id}.jpg")
    await photo.download(destination_file=file_path)

    img = cv2.imread(file_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if os.path.exists(file_path):
        os.remove(file_path)
    # parsed_data = json.loads(data)
    # print('parsed_data', parsed_data)
    # print('data', data)
    if not data:
        await message.answer(text="❌❌ Bunday QR kod topilmadi")
        return

    # unique_code = parsed_data.get('unique_code')
    # user_name = parsed_data.get('user_name')
    # print('unique_code', unique_code)

    qr_codes = await db.select_qr_codes(information=data)
    if not qr_codes:
        await message.answer(text="❌❌ QR kod topilmadi")
    else:
        qr_code = qr_codes[0]
        user_name = qr_code['user_name']
        qr_is_active = qr_code['is_active']
        if qr_is_active:
            await db.update_qr_code(qr_code_id=qr_code['id'], is_active=False)
            await message.answer(text=f"✅✅ QR kod muvaffaqiyatli ro'yxatdan o'tkazildi.\n"
                                      f"QR kod egasi: {user_name}")
        else:
            await message.answer(text=f"🛑🛑 Kechirasiz, bu QR koddan ilgari foydalanilgan.\n"
                                      f"QR kod egasi: {user_name}")
