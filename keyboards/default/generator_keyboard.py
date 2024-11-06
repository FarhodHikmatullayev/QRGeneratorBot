from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

generate_qr_code_default_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🛠️ Generate QR")
        ]
    ]
)
