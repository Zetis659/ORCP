import sys
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main_kb = [
    [KeyboardButton(text="🚀 Старт 🚀"), KeyboardButton(text="🆘 Помощь 🆘")],
    [KeyboardButton(text="Инфо о боте 🤖"), KeyboardButton(text="Контакты 📟")],
]

main = ReplyKeyboardMarkup(
    keyboard=main_kb,
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт ниже",
)

git = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Telegram", url="https://t.me/zetis_zs")],
        [InlineKeyboardButton(text="GitHub", url="https://github.com/Zetis659")],
    ]
)

details = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Подробнее", callback_data="details")]]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="back")]]
)

brands = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="BAIC", callback_data="baic"),
            InlineKeyboardButton(text="BYD", callback_data="byd"),
            InlineKeyboardButton(text="Changan", callback_data="changan"),
        ],
        [
            InlineKeyboardButton(text="Chery", callback_data="chery"),
            InlineKeyboardButton(text="Dongfeng", callback_data="dongfeng"),
            InlineKeyboardButton(text="Exeed", callback_data="exeed"),
        ],
        [
            InlineKeyboardButton(text="FAW", callback_data="faw"),
            InlineKeyboardButton(text="GAC", callback_data="gac"),
            InlineKeyboardButton(text="Geely", callback_data="geely"),
        ],
        [
            InlineKeyboardButton(text="Great Wall", callback_data="great_wall"),
            InlineKeyboardButton(text="Haval", callback_data="haval"),
            InlineKeyboardButton(text="Hongqi", callback_data="hongqi"),
        ],
        [
            InlineKeyboardButton(text="JAC", callback_data="jac"),
            InlineKeyboardButton(text="Jetta", callback_data="jetta"),
            InlineKeyboardButton(text="Kaiyi", callback_data="kaiyi"),
        ],
        [
            InlineKeyboardButton(text="Lifan", callback_data="lifan"),
            InlineKeyboardButton(text="Livan", callback_data="livan"),
            InlineKeyboardButton(text="Lixiang", callback_data="lixiang"),
        ],
        [
            InlineKeyboardButton(text="Omoda", callback_data="omoda"),
            InlineKeyboardButton(text="Tank", callback_data="tank"),
            InlineKeyboardButton(text="Vortex", callback_data="vortex"),
        ],
        [
            InlineKeyboardButton(text="Voyah", callback_data="voyah"),
            InlineKeyboardButton(text="Zeekr", callback_data="zeekr"),
            InlineKeyboardButton(text="Zotye", callback_data="zotye"),
        ],
    ]
)
