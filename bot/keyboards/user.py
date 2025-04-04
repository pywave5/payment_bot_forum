from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def get_start_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎫 Chipta sotib olish")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def buy_ticked_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎫 Chipta sotib olish")]
        ],
        resize_keyboard=True
    )
    return keyboard

def request_number() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📞 telefon raqamni jo'natish", request_contact=True)],
    ], resize_keyboard=True, one_time_keyboard=True)

    return keyboard

def get_inline_rates() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="STANDART - 49 000 so'm", callback_data="rate_standart")],
        [InlineKeyboardButton(text="COMFORT - 300 000 so'm", callback_data="rate_comfort")],
        [InlineKeyboardButton(text="BUSINESS - 480 000 so'm", callback_data="rate_business")],
        [InlineKeyboardButton(text="VIP - 720 000 so'm", callback_data="rate_vip")],
        [InlineKeyboardButton(text="PLATINUM - 2 800 000 so'm", callback_data="rate_platinum")]
    ])
    return keyboard

def get_payment_methods() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="💳 Payme")],
    ], resize_keyboard=True, one_time_keyboard=True)

    return keyboard

def get_pay_link(url: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 To'lov", url=url)]
    ])

    return ikb