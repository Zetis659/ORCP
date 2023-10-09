import sys
import asyncio
import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import Bot.core.keyboards as kb
from aiogram import Bot
from Bot.core.settings import TOKEN_ID
from Bot.core.predictions import yolo_results
from Bot.core.detection import yolo_detect
import datetime

router = Router()

bot = Bot(token=TOKEN_ID, parse_mode="HTML")


@router.message(F.text == "/start")
async def first_start(message: Message):
    await message.answer(
        """
<b>Добро пожаловать!</b> \nДанный бот 🤖 поможет вам <b>определить марку и модель</b> автомобиля 🚗, а так же его <b>стоимость</b> 💸 по фотографии 📸\n
В данный момент бот 🤖 <b>ориентирован на китайские автомобили</b> 🇨🇳
Поддерживает 134 модели 🚘 от 24 брендов, таких как: Haval, Geely, Chery, Changan, Great Wall, Lifan и многих других\n
Для начала работы <b>воспользуйтесь кнопками меню</b> 🖲️ или <b>отправьте боту 🤖 фотографию 📸 авто</b> 🚘\n
<b>Удачи и приятного использования!</b> 🚗🤖🔍""",
        reply_markup=kb.main,
    )


@router.message(F.text == "🚀 Старт 🚀")
async def cmd_start(message: Message):
    await message.answer(
        """
Просто <b>отправьте фото</b> 📸 интересующего вас <b>АВТОМОБИЛЯ</b> 🚘 данному боту 🤖 и <b>он определит</b>:
<b>МАРКУ и МОДЕЛЬ</b> данного <b>АВТО</b>, а так же укажет его <b>среднюю стоимость</b> 💸
\nДля уточнения деталей 🔍 в съёмке авто нажмите на кнопку: <b>🆘 Помощь 🆘</b>
\nДля просмотра списка поддерживаемых моделей авто, нажмите на кнопку: <b>Инфо о боте 🤖</b>"""
    )


@router.message(F.text == "🆘 Помощь 🆘")
async def cmd_help(message: Message):
    await message.answer(
        'Для того, чтобы бот 🤖 смог корректно определить модель авто 🚘 нужно фотографировать экстерьер, то есть автомобиль "c улицы" 🏘️'
    )
    await asyncio.sleep(4)
    await message.answer("✅ <b>Хорошие примеры:</b>")
    await message.answer_photo(
        photo="AgACAgIAAxkBAAMSZRaTgzKD5rKta0S2Z8Ra94sXHzEAAhTRMRu_kbhI8xCBnj-995wBAAMCAAN5AAMwBA"
    )
    await asyncio.sleep(2)
    await message.answer_photo(
        photo="AgACAgIAAxkBAAMUZRaT7SFIJQj5BaCWWnLmixuVDSAAAhjRMRu_kbhIMdoTFntTqn4BAAMCAAN5AAMwBA"
    )
    await asyncio.sleep(2)
    await message.answer("❌ <b>Плохие примеры:</b>")
    await message.answer_photo(
        photo="AgACAgIAAxkBAAMWZRaUJjHN2Tj6AuE6NXG2-UQwUt0AAhnRMRu_kbhIx9ANz1VnmBQBAAMCAAN5AAMwBA",
        caption="❌ Часть автомобиля перекрыто другими объектами ❌",
    )
    await asyncio.sleep(3.5)
    await message.answer_photo(
        photo="AgACAgIAAxkBAAMYZRaUMRjJWY5E5yAkYpjpMKYw5C4AAhrRMRu_kbhI86w1OqHaYJoBAAMCAAN5AAMwBA",
        caption="❌ Автомобиль сфотографирован НЕ ЦЕЛИКОМ ❌",
    )
    await asyncio.sleep(3.5)
    await message.answer_photo(
        photo="AgACAgIAAxkBAAMaZRaUPmn7CPEby_OZm3lvvYWdJiQAAhzRMRu_kbhI0nsu0YjtM78BAAMCAAN5AAMwBA",
        caption="❌ Фото салона НЕ подходят для данного бота 🤖 ❌",
    )


@router.message(F.text == "Инфо о боте 🤖")
async def cmd_start(message: Message):
    await message.answer(
        """
В данный момент бот 🤖 ориентирован на <b>китайские автомобили</b>🇨🇳
Поддерживает 134 модели 🚘 от 24 брендов, таких как: Haval, Geely, Chery, Changan, Great Wall, Lifan и многих других.
\n<b>Для просмотра доступных брендов</b> нажмите кнопку: <b>"Подробнее"</b> ⤵
""",
        reply_markup=kb.details,
    )


@router.message(F.text == "Контакты 📟")
async def cmd_start(message: Message):
    await message.answer(
        """
Контакты ⤵
""",
        reply_markup=kb.git,
    )


@router.callback_query(F.data == "details")
async def details(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer(
        """
Список доступных на данный момент брендов авто 🚘
Для получения информации о бренде, а так же о списке доступных моделей, которые может распознать данный бот 🤖 - <b>нажмите на бренд:</b> ⤵""",
        reply_markup=kb.brands,
    )


@router.callback_query(F.data == "back")
async def details(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer(
        """
Список доступных на данный момент брендов авто 🚘
Для получения информации о бренде, а так же о моделях, которые может распознать данный бот 🤖 - выберите бренд:""",
        reply_markup=kb.brands,
    )


@router.callback_query(F.data == "baic")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.upper()}!")
    await callback.message.answer(
        '<b>Логотип бренда BAIC:</b>\nОригинальное произношение "Бэй Ци"\nОбычно произносят как "Баик"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBCWUWtvOFxWf41k5IXU4iYlODETuzAAL70TEbv5G4SBX4h9TEic2QAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей BAIC:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBDGUW1z1pAe3A2exAZeJKTpd5NpWdAAJt0zEbv5G4SKGzLrr9YHBfAQADAgADeQADMAQ",
        caption="BAIC U5 Plus",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBD2UW19TJXgABYmY-YRKuH4cwTWD-ngACcNMxG7-RuEjfP8qgkTzRbwEAAwIAA3kAAzAE",
        caption="BAIC X35",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "byd")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.upper()}!")
    await callback.message.answer(
        '<b>Логотип бренда BYD:</b>\nОригинальное произношение "Би Я Ди" или "Би Уай Ди"\nОбычно произносят как "Бид"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBxmUW5QQQ1r7O4AZGPlXwhX5yPQKBAAKs0zEbv5G4SNopRyK47nEQAQADAgADeAADMAQ"
    )
    await callback.message.answer("<b>Список моделей BYD:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIB4GUW5t-fU17WN8s__wGeEGsHAxi2AAKz0zEbv5G4SIWTpZ0ik4r6AQADAgADeQADMAQ",
        caption="BYD F3 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIB4mUW5u7K06TRrBtTdFKDnIykMnJxAAK00zEbv5G4SIFHnoD1DMKoAQADAgADeQADMAQ",
        caption="BYD HAN I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIB5GUW5vpXhS0hNW3_0oPok4bmq7Q-AALB0zEbv5G4SKGaahGecChKAQADAgADeQADMAQ",
        caption="BYD Song Plus",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDEGUX9pEToCde49wuizIhYr8vLT32AAJ0zzEbMtTASNzYH8e_svMAAQEAAwIAA3kAAzAE",
        caption="BYD TANG II",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "changan")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Changan:</b>\nОригинальное произношение "Чан Ань", в переводе - "надежность, проверенная временем"\nОбычно произносят как "Чанган"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICLWUW65RgIuj_q6UcYOkuYQyRh3LfAAL50zEbv5G4SDY_tU_FIrOmAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Changan:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICf2UW9T3TNsP4T-kKLe4PIVOKa4RjAAL60zEbv5G4SKYHZQXHt180AQADAgADeQADMAQ",
        caption="Changan Alsvin",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICgWUW9Uw7tk6_UR4CGqH6usvHErjIAAL70zEbv5G4SNiTX3zFiCP7AQADAgADeQADMAQ",
        caption="Changan CS35",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICg2UW9VvQCRgAAS6oKITqEhk1UHhJhQAC_dMxG7-RuEgV52_9O32sUwEAAwIAA3kAAzAE",
        caption="Changan CS35 Plus I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIChWUW9WibB0KT5_kEsIqHENc3JLI3AAL_0zEbv5G4SHUNnIKbGgH-AQADAgADeQADMAQ",
        caption="Changan CS35 Plus I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICh2UW9XsNJPwSPqfGbKM5-S93lCNiAAPUMRu_kbhIOjTRqL2FQRkBAAMCAAN5AAMwBA",
        caption="Changan CS55 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDQmUX-BdOCtKiLN_HWYfyTEcbKLbpAAKEzzEbMtTASEuNiHoJvzALAQADAgADeQADMAQ",
        caption="Changan CS55 Plus I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICi2UW9ZcR5x8vdZXHF9hHwA85EpGfAAIP1DEbv5G4SLqb2fMhpXquAQADAgADeQADMAQ",
        caption="Changan CS55 Plus I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICjWUW9abHKFj5QLb8q16RdLcp6qjoAAIe1DEbv5G4SBcfqZNUHDI8AQADAgADeQADMAQ",
        caption="Changan CS75 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICj2UW9bIilHa2i2K19mh2tsXzF6NBAAIh1DEbv5G4SKHa8tywEaP1AQADAgADeQADMAQ",
        caption="Changan CS75 II",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICkWUW9catUdMY6ueGrO7gLaA3O0rRAAIi1DEbv5G4SB377kgei-jDAQADAgADeQADMAQ",
        caption="Changan CS85",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICk2UW9dNJlilgoVncQBx6__dc8hA5AAIm1DEbv5G4SHW5kOkUJB5sAQADAgADeQADMAQ",
        caption="Changan CS95 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIClWUW9eTuV4Z0CVADpD71H1pJ9WQNAAIo1DEbv5G4SNSRP70IAAFeaAEAAwIAA3kAAzAE",
        caption="Changan Eado Plus",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICl2UW9fFpGTrs2QeA_MuiVHEJVfDeAAIq1DEbv5G4SPMVKn2RExMXAQADAgADeQADMAQ",
        caption="Changan Hunter",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICmWUW9f1HyqCBxTI1-4WtiZh2-6DbAAIr1DEbv5G4SPL_GPzNLmA1AQADAgADeQADMAQ",
        caption="Changan UNI-K",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICm2UW9gsufUP8H5aljwpJ5TAtwzolAAIs1DEbv5G4SP6bYoA8HJJKAQADAgADeAADMAQ",
        caption="Changan UNI-T",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAICnWUW9h7bj9ev_d1k5SrJ5iUESuckAAIt1DEbv5G4SJII0Wv5iLqzAQADAgADeQADMAQ",
        caption="Changan UNI-V",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "chery")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Chery:</b>\nОригинальное произношение "Ци Жуй", в переводе - "хорошая примета"\nОбычно произносят как "Чери"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAID3GUYCG_vwFJj7DQjqdH39GRgQ3CcAAIR0DEbMtTASHPLtIXtypEeAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Chery:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDsGUYBbOKZZWCq2Uoke64svzuyhshAALlzzEbMtTASHQkfAlaCsYRAQADAgADeQADMAQ",
        caption="Chery Amulet I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDsmUYBcfCUucdFDSssA3_i1E2is_iAALozzEbMtTASPRLUT_yjpgwAQADAgADeQADMAQ",
        caption="Chery Arizo 8",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDtGUYBdAZE4S_iisPcFS7aUCaJq2dAALpzzEbMtTASJO3dL5FMoScAQADAgADeQADMAQ",
        caption="Chery Bonus",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDtmUYBdgyow5opYK-qorGHwUFgFbmAALqzzEbMtTASOege7Sj9JEWAQADAgADeAADMAQ",
        caption="Chery Fora",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDuGUYBeHv2t7E_QfXNp9n6TDp-j_4AALrzzEbMtTASIrwZ6XSgau2AQADAgADeQADMAQ",
        caption="Chery Indis I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDumUYBejXyYDotxykcBtdrAn8VPBhAALtzzEbMtTASOjOs1mG2kDzAQADAgADeQADMAQ",
        caption="Chery Kimo",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDvGUYBfC0LZY5U4phbJBSjoPFxaIpAALuzzEbMtTASO7A1DywCN7VAQADAgADeQADMAQ",
        caption="Chery M11",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDvmUYBfnTne1R91Ssq5WCSmkl6aCeAALwzzEbMtTASAddlb935rDVAQADAgADeAADMAQ",
        caption="Chery Tiggo I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDwGUYBgoTfrp9QIUS0qXa3MTc-M92AALxzzEbMtTASEMOuX1-zgcMAQADAgADeAADMAQ",
        caption="Chery Tiggo I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDwmUYBhgW7gNuIX0I6g4DWj7FidKiAALyzzEbMtTASG8X8SyydJ-dAQADAgADeQADMAQ",
        caption="Chery Tiggo 3 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDxGUYBi3xCjKxmX4NyKmWjF3LaYrTAAL0zzEbMtTASKj6KK9UOdClAQADAgADeQADMAQ",
        caption="Chery Tiggo 4 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDxmUYBjPejyshY-EmAaX3AAE1USW-2wAC9c8xGzLUwEgzWpviM_NYCQEAAwIAA3kAAzAE",
        caption="Chery Tiggo 4 Pro",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDyGUYBj1iJ4MwnMr9q9Q5_C_sBj1BAAL3zzEbMtTASISfm-0UKkBgAQADAgADeQADMAQ",
        caption="Chery Tiggo 5 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDymUYBkZ446L_RetSp13kLUR7qhbeAAL4zzEbMtTASAABIC5GBgQuCwEAAwIAA3kAAzAE",
        caption="Chery Tiggo 7 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDzGUYBk5qrVw4tjKTcLX6Hk2KA-HsAAL5zzEbMtTASM6yCB4aEI-yAQADAgADeQADMAQ",
        caption="Chery Tiggo 7 Pro",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIDzmUYBlVx60niIxBtBdm21etMtqfzAAL6zzEbMtTASDKQbVXzENV1AQADAgADeQADMAQ",
        caption="Chery Tiggo 7 Pro Max",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAID0GUYBludeBT54voDF6AQhNKUTVVqAAL7zzEbMtTASEdL9tBRoxMWAQADAgADeQADMAQ",
        caption="Chery Tiggo 8 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAID0mUYBmLZTbu6NxabxkxpsovZLjhwAAL8zzEbMtTASCJXatMD3-emAQADAgADeQADMAQ",
        caption="Chery Tiggo 8 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAID1GUYBmgGaCZf4Ys9R0tkQGHw9CcxAAL9zzEbMtTASGXoJotGaIu2AQADAgADeQADMAQ",
        caption="Chery Tiggo 8 Pro I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAID1mUYBm72O379OfdkmJ9bqzoRPVfbAAL-zzEbMtTASPfPUniI16t6AQADAgADeQADMAQ",
        caption="Chery Tiggo 8 Pro I (China Market)",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAID2GUYBnaxnnwkAAEaLvp1xOtBpODE3QAC_88xGzLUwEgeeuC0EKAw9wEAAwIAA3kAAzAE",
        caption="Chery Tiggo 8 Pro E+",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAID2mUYBn9Itk51irgM5gHpDtk-4uPkAAPQMRsy1MBIaxNx6gb02yYBAAMCAAN5AAMwBA",
        caption="Chery Tiggo 8 Pro Max",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "dongfeng")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Dongfeng:</b>\nОригинальное произношение "Дун Фэн", в переводе - "восточный ветер"\nОбычно произносят как "Донг Фэнг"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIEXGUYFQ9hgrxJvGBQu1p64cyp5FhTAAKV0DEbMtTASBnCSZgQzL98AQADAgADeAADMAQ"
    )
    await callback.message.answer("<b>Список моделей Dongfeng:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIEXmUYFRYBZlQUg0lcweJ3zjS8FZ6mAAKT0DEbMtTASM_somi1eXJ7AQADAgADeQADMAQ",
        caption="Dongfeng 580",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIEYGUYFSGDUUkjlFs45206YZak-INHAAKU0DEbMtTASBy3VMUj3JDkAQADAgADeQADMAQ",
        caption="Dongfeng DF6",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "exeed")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Exeed:</b>\nОбычно произносят как "Эксид"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIER2UYEpAutrjTBW7jT5Mws8DU1OwpAAKF0DEbMtTASEdtGVtwRE2NAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Exeed:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIEPWUYEkgjCxU7Myp7rcJSpqbttBJvAAJ-0DEbMtTASBGBEo5S7UfFAQADAgADeQADMAQ",
        caption="Exeed LX",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIEP2UYElEvi7Vhcd8JB12ZmDRm1dwaAAJ_0DEbMtTASBfRYy0S9Hc9AQADAgADeQADMAQ",
        caption="Exeed RX",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIEQ2UYEl4oAAHCj5s5J2OAwsPFHiwb5QACgdAxGzLUwEhVYdmZfPUBsAEAAwIAA3kAAzAE",
        caption="Exeed TXL I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIEQWUYElc42vhAtoXRn83LPX0pbFqiAAKA0DEbMtTASO6gBjxYa3PjAQADAgADeQADMAQ",
        caption="Exeed TXL I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIERWUYEmnC3-G252BV3kQUFFjxnLc1AAKC0DEbMtTASB5QMHKJpE6bAQADAgADeQADMAQ",
        caption="Exeed VX I",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "faw")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.upper()}!")
    await callback.message.answer(
        '<b>Логотип бренда FAW:</b>\nОбычно произносят как "Фав"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE3mUZTphmhc56SKkyiTM30G2VIdoHAAKS0TEb1ybQSMiAIgk0Mo9AAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей FAW:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE4GUZTrrFpPqirRxn5aWLlLimnJBeAAKT0TEb1ybQSMo-02vfBlvnAQADAgADeQADMAQ",
        caption="FAW Bestune B70",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE4mUZTsIiUFQTw-pi_O__h58_DzBwAAKV0TEb1ybQSCN1g0kKoI5HAQADAgADeQADMAQ",
        caption="FAW Bestune T55",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE5GUZTsjcJN4cvEXvZynY1X90JyyrAAKW0TEb1ybQSDDZvWmi-_hkAQADAgADeQADMAQ",
        caption="FAW Bestune T77",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE5mUZTs5YJ5_2_Iow2SuET7JUpEBcAAKX0TEb1ybQSLnJL1q807g6AQADAgADeQADMAQ",
        caption="FAW Bestune T99 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE6GUZTtVI8KGWkLggIDUYgqfgJAXSAAKY0TEb1ybQSDxsw37SLU3vAQADAgADeQADMAQ",
        caption="FAW Besturn X40 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE6mUZTtuwOD8E7GpHFFoVC4MAAVSbUwACmdExG9cm0Ej2Ijeh3JrtkwEAAwIAA3kAAzAE",
        caption="FAW Besturn X80 I Рестайлинг",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "gac")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.upper()}!")
    await callback.message.answer(
        '<b>Логотип бренда GAC:</b>\nОригинальное произношение "Гуан Ци", в переводе - "благополучие"\nОбычно произносят как "Гак" или "Джи Эй Си"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE_2UZUQ04dFYMSEvgrA8REPWDqqNkAAKs0TEb1ybQSLMIzUOZfQrLAQADAgADeAADMAQ"
    )
    await callback.message.answer("<b>Список моделей GAC:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFAWUZUSIkXKjjur7FmVd_7-iqJtdvAAKt0TEb1ybQSL8BhQH0agGnAQADAgADeQADMAQ",
        caption="GAC GN8 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFA2UZUSkJbi3eYhUygvfVCsIg7EOzAAKu0TEb1ybQSJP8fRELGOHRAQADAgADeQADMAQ",
        caption="GAC GS8 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFBWUZUTiM22k6B5UV8-6ER9_QlVIpAAKv0TEb1ybQSMawD2FpT8HcAQADAgADeQADMAQ",
        caption="GAC GS8 II",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "geely")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Geely:</b>\nОригинальное произношение "Цзи Ли", в переводе - "сладкая жизнь" или "благополучие"\nОбычно произносят как "Джили"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFXGUZWBo71DhBg9qxky8_W3wLPPBcAAL40TEb1ybQSGMH6rhtUv_dAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Geely:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFOmUZV1icJ5oJNMcfIRCBvCd9MYFDAALj0TEb1ybQSIWQpC10LXoUAQADAgADeQADMAQ",
        caption="Geely Atlas I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFPGUZV15sxeGUngABH7OIbJ2EdUYXugAC5NExG9cm0EhnhtB7pCLb6wEAAwIAA3kAAzAE",
        caption="Geely Atlas Pro",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFPmUZV2Q8n_9s3iTh5A82C2dricW0AALl0TEb1ybQSE6Oiu-BKtu6AQADAgADeQADMAQ",
        caption="Geely Coolray I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFQGUZV2lh3nOYhPZ9r5I4-KfjrD7bAALn0TEb1ybQSDXjp5HahCr1AQADAgADeQADMAQ",
        caption="Geely Emgrand",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFQmUZV2_EwD9dgbQxD76TsRRoEsuLAALo0TEb1ybQSJci8xMAAU5DOQEAAwIAA3kAAzAE",
        caption="Geely Emgrand 7 II",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFRGUZV3RINimH0Vsbj6m3HSska1wFAALp0TEb1ybQSJtZEjVdyT4nAQADAgADeAADMAQ",
        caption="Geely Emgrand X7 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFRmUZV3q1Fm2ZDXVKQ6-xSj9XfM5UAALq0TEb1ybQSD0JyoNRjqzeAQADAgADeQADMAQ",
        caption="Geely Emgrand X7 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFSGUZV4SuieYMg0o0womTaXVQyAQOAALs0TEb1ybQSI9VnUkzkRiAAQADAgADeQADMAQ",
        caption="Geely Emgrand X7 I Рестайлинг 2",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFSmUZV4uY8OI8rEpcywT5vh0AAeT90wAC7dExG9cm0Egym_qAaztDIwEAAwIAA3kAAzAE",
        caption="Geely GC6",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFTGUZV5HWWg2qr89RojN_QmGW3KteAALu0TEb1ybQSBgEadL4aWfNAQADAgADeQADMAQ",
        caption="Geely Icon",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFTmUZV5fYZNKTBFqUwWXTarS62HB3AALv0TEb1ybQSDypggqt8KQaAQADAgADeQADMAQ",
        caption="Geely MK I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFUGUZV52NFGo3pfuWP2AvsxCj2Pf6AALw0TEb1ybQSKjd9YvwztXfAQADAgADeQADMAQ",
        caption="Geely MK Cross I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFUmUZV6NHmmk0s3dveBTbLXclElh9AALx0TEb1ybQSGkz8tZnT-vWAQADAgADeQADMAQ",
        caption="Geely Monjaro",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFVGUZV6pybCRavJ4vP4VFH4DEdCNiAALy0TEb1ybQSLwXWT4_PsWbAQADAgADeQADMAQ",
        caption="Geely Okavango",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFVmUZV7GMK1snVfeBKGA1pDdwZbAlAALz0TEb1ybQSNGzx8iqWHRWAQADAgADeQADMAQ",
        caption="Geely Preface",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFWGUZV7geITez8ZUVSj0EUU1gZU8wAAL00TEb1ybQSA96lRSWFRr5AQADAgADeQADMAQ",
        caption="Geely Tugella I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFWmUZV74e6H76SQaPam4AAe4OYyNvlwAC9dExG9cm0EhPOYI6zRx7AQEAAwIAA3kAAzAE",
        caption="Geely Tugella I Рестайлинг",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "great_wall")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.upper()}!")
    await callback.message.answer(
        '<b>Логотип бренда Great Wall:</b>\nОригинальное произношение "Чан Чэн", в переводе - "Великая Китайская стена"\nОбычно произносят как "Грейт Уол"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFiWUZYDX7GsrcMEE-4XOrHaqKUBXTAAIb0jEb1ybQSKW7XH-QjVIVAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Great Wall:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFi2UZYE3_5sYtwSt_tKQWnQnqS6kbAAIc0jEb1ybQSAb6b8DxIn9nAQADAgADeQADMAQ",
        caption="Great Wall Hover",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFjWUZYFIDc36YMb7uD-2tYA5U1wWoAAId0jEb1ybQSEZfoEl7s1o4AQADAgADeQADMAQ",
        caption="Great Wall Hover H3 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFj2UZYFty_qKY1abEeg1J-DJLBzsiAAIe0jEb1ybQSCGagmD2E_sWAQADAgADeQADMAQ",
        caption="Great Wall Hover H5",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFkWUZYGRpeDphwM0jNk4DbRIqA9ZWAAIf0jEb1ybQSEr7c2X_qHI_AQADAgADeQADMAQ",
        caption="Great Wall Poer I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFk2UZYGtPrUaPrllpNi5ccFbOojW4AAIg0jEb1ybQSAeQEch9W5uzAQADAgADeQADMAQ",
        caption="Great Wall Poer King Kong",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFlWUZYHUDX717U2xUBGv_2H2wteHfAAIh0jEb1ybQSBvxUyKtzCgLAQADAgADeQADMAQ",
        caption="Great Wall Safe",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "haval")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Haval:</b>\nОригинальное произношение "Ха Фу", в переводе - "вольный ветер"\nОбычно произносят как "Хавал" или "Хавэйл"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFyGUZZkEuvC8eMwAB3GXR6G6bLLdycAACUdIxG9cm0Ejy0yvpdD8LnAEAAwIAA3kAAzAE"
    )
    await callback.message.answer("<b>Список моделей Haval:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFymUZZlixFNl8tqKoEgnBMrMaOaplAAJS0jEb1ybQSPLVHQABjIK6sgEAAwIAA3kAAzAE",
        caption="Haval Dargo",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFzGUZZmA-evn6oJSJRny-S1fK1jtzAAJT0jEb1ybQSAmtSNLWizvLAQADAgADeQADMAQ",
        caption="Haval F7 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIFzmUZZmZG0W4ZZGPn-Gl7s1vqTgWzAAJU0jEb1ybQSFpvutjmIGUjAQADAgADeQADMAQ",
        caption="Haval F7 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIF0GUZZm18J9ML19O_Hy6NamhO-N9bAAJV0jEb1ybQSINp3ejL-eztAQADAgADeQADMAQ",
        caption="Haval F7x I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIF0mUZZnQsC4I4L1Ls3jf2BlFIbLjJAAJW0jEb1ybQSGsEEx2VbkcqAQADAgADeQADMAQ",
        caption="Haval F7x I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIF1GUZZnuzxvTizU81fvecSlZYI3_1AAJX0jEb1ybQSM4rrd2LvLU4AQADAgADeQADMAQ",
        caption="Haval H5 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIF1mUZZoDn4LWETcLp5rUfqtvukeECAAJY0jEb1ybQSJMIIVR6wkprAQADAgADeQADMAQ",
        caption="Haval H6 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIF2GUZZob2M84g3rKQRgTYTItaBSCZAAJZ0jEb1ybQSNhvLsoFpdMjAQADAgADeQADMAQ",
        caption="Haval H6 III",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIF2mUZZo60R91di_oJ-4HpE1BoWM3ZAAJa0jEb1ybQSMs8uydIFHraAQADAgADeQADMAQ",
        caption="Haval H9 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIF3GUZZpMn7gP2Y-ur4MJDJoS95hieAAJb0jEb1ybQSN8s5Fl8iQStAQADAgADeQADMAQ",
        caption="Haval Jolion I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIF3mUZZpoINWYtwv0gNXtY_VN_HpgaAAJc0jEb1ybQSOKvW4i8XFPnAQADAgADeQADMAQ",
        caption="Haval M6",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "hongqi")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Hongqi:</b>\nОригинальное произношение "Хун Ци", в переводе - "красное знамя"\nОбычно произносят как "Хонгки"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGAAFlGWv9xRCtPkrJ6M7zHXdMffqrtwAChdIxG9cm0Eh4mOKUmsw5YwEAAwIAA3gAAzAE"
    )
    await callback.message.answer("<b>Список моделей Hongqi:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGAmUZbBZTrTzQPrDIYSZZNHawGRhKAAKH0jEb1ybQSMkG6b48LHW_AQADAgADeQADMAQ",
        caption="Hongqi E-HS9",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGBGUZbB5iwiCJlFOe-Pqk_m2IisByAAKI0jEb1ybQSH3c5dsavpwRAQADAgADeQADMAQ",
        caption="Hongqi H5 II",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGBmUZbCVHeY-jsn1xC8Nm3Lr2GgY_AAKJ0jEb1ybQSAp6aLT51oCJAQADAgADeQADMAQ",
        caption="Hongqi H9",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGCGUZbCuD0WdZFA1pKmDs785WRrTmAAKK0jEb1ybQSDTgvftFqw7bAQADAgADeQADMAQ",
        caption="Hongqi HQ9",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGCmUZbDI5vCpiIk2VvkgszTsQ0aXjAAKL0jEb1ybQSMcD8yU987K2AQADAgADeQADMAQ",
        caption="Hongqi HS5",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "jac")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.upper()}!")
    await callback.message.answer(
        '<b>Логотип бренда JAC:</b>\nОригинальное произношение "Цзян Хуэй"\nОбычно произносят как "Джак"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGJmUZcA1hWwHlJCbVRdiwCifKaRnmAAKd0jEb1ybQSOkxtbGmz2dcAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей JAC:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGKGUZcBdtcGsFSgnOKZG2uCDq7MsiAAKf0jEb1ybQSGYhVYD7FIosAQADAgADeQADMAQ",
        caption="JAC J7 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGKmUZcByq6YMac7zSKKQ_syFhBwNVAAKg0jEb1ybQSLgWXybwqAUQAQADAgADeQADMAQ",
        caption="JAC JS6",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGLGUZcCOEwU_Sl5zKIbVOh6-rgFYGAAKh0jEb1ybQSMbx-XqR43UuAQADAgADeQADMAQ",
        caption="JAC T6",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "jetta")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Jetta:</b>\nОбычно произносят как "Джэта"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGRGUZcwd7_hYGkiFDXQjJHVLeXNzuAAKt0jEb1ybQSPqGqVfOuQKCAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Jetta:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGRmUZcxbmgcEICcyPEZQJr35rBlfaAAKv0jEb1ybQSPU2qZJMPAs6AQADAgADeQADMAQ",
        caption="Jetta VA3",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGSGUZcx3med7fP3fCScmCSAu8n5YgAAKw0jEb1ybQSJxocPW8mC6nAQADAgADeQADMAQ",
        caption="Jetta VS5",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGSmUZcyT4PJNtkdIRDuV8ylrc-skZAAKx0jEb1ybQSOE4e59X2FsOAQADAgADeAADMAQ",
        caption="Jetta VS7",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "kaiyi")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Kaiyi:</b>\nОригинальное произношение "Кай И", в переводе - "триумфальные крылья"\nОбычно произносят как "Каи"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGYWUZdNAFLj0otbtqxbymooGYfHzbAAK70jEb1ybQSKKpjuIpsbanAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Kaiyi:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGY2UZdNjHu88yYKkxPlzkdI2CXUNqAAK40jEb1ybQSBZsOqeT-lFhAQADAgADeQADMAQ",
        caption="Kaiyi E5",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "lifan")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Lifan:</b>\nСозвучно с китайским "Ли Фань", в переводе - "идти на всех парусах"\nОбычно произносят как "Лифан"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGn2UajP0xBDpa4R9hn3OWtrysUUjdAAJ0zDEbTCjQSGu9ICD2B5lZAQADAgADeAADMAQ"
    )
    await callback.message.answer("<b>Список моделей Lifan:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGoWUajRmQctHOxQ7FhbEuAAFmzZgylAACdswxG0wo0EgpmLpxVeOD9QEAAwIAA3kAAzAE",
        caption="Lifan Breez",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGo2UajSAXHDM7WdZsl1RfTIUR8A4pAAJ3zDEbTCjQSDXs3zBXQ2oUAQADAgADeAADMAQ",
        caption="Lifan Cebruim",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGpWUajSabgQUyAguBX_GviBdO7jP4AAJ4zDEbTCjQSPggzr7vMBAHAQADAgADeAADMAQ",
        caption="Lifan Smily",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGp2UajS1lGqwHWCQgkALxAAFY7VBJiQACecwxG0wo0EiOwuOpCCzvngEAAwIAA3gAAzAE",
        caption="Lifan Solano I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGqWUajTYYNOeBiPJHg7Fn-giWoIFTAAJ6zDEbTCjQSCCTaY1JZFNaAQADAgADeQADMAQ",
        caption="Lifan Solano II",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGq2UajT4Jim4OSCKuZKEOQ1wElnbsAAJ7zDEbTCjQSJ-Wwe-hGKzoAQADAgADeQADMAQ",
        caption="Lifan X50",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGrWUajUbna_mnZ265lazODDWcfs1FAAJ8zDEbTCjQSOMFVsHCgQABNwEAAwIAA3kAAzAE",
        caption="Lifan X60 I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGr2UajU8l3JD-clxMJ7vqs5mqb54JAAJ9zDEbTCjQSAMyTfgZQQORAQADAgADeAADMAQ",
        caption="Lifan X60 I Рестайлинг",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGsWUajVo-DvOPk_Fx64Yucru0UKX2AAJ_zDEbTCjQSP-1kFWwxm_iAQADAgADeQADMAQ",
        caption="Lifan X60 I Рестайлинг 2",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "livan")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.upper()}!")
    await callback.message.answer(
        '<b>Логотип бренда Livan:</b>\nLIVAN - аббревиатура английсокго словосочетания:  «свобода, воображение, авангард и действие без остановки»\nОбычно произносят как "Ливан" или "Ливэн"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGzWUakdh6CNZkgvOayTOZQjYo-Li6AAKczDEbTCjQSHYSanYXfgg-AQADAgADeAADMAQ"
    )
    await callback.message.answer("<b>Список моделей Livan:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIGz2Uakd9W8JM5sbxPe92mbfexs6ehAAKZzDEbTCjQSAABKjYRA6mU4QEAAwIAA3kAAzAE",
        caption="Livan X3 Pro",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "lixiang")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда LiXiang:</b>\nОригинальное произношение "Ли Сянь", в переводе - "мечта"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIG52UalV7nzJkKGROnUji31Ba_np4NAAKqzDEbTCjQSCA8Lubmvq0gAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей LiXiang:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIG6WUalWfdJ5acdx_h4PSwM9y4WXT0AAKezDEbTCjQSMlnEJHNPVgKAQADAgADeQADMAQ",
        caption="LiXiang L7",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIG62UalXAVgK_328RGkdObaqn44RDtAAKpzDEbTCjQSBS3kbkzOpOHAQADAgADeQADMAQ",
        caption="LiXiang L8",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIG7WUalXgeLUPIn6TkZdL7CT44iaOuAAKmzDEbTCjQSIQq4jFIZbOSAQADAgADeQADMAQ",
        caption="LiXiang L9",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIG72UalYM13eZ0aqZve_yL4VbUmit6AAKozDEbTCjQSFPlbjNxu28wAQADAgADeQADMAQ",
        caption="LiXiang One",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "omoda")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Omoda:</b>\nСозвучно с китайским "Оу Мэнда", в переводе - "новая мода"\nОбычно произносят как "Омода"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHAAFlGpmdFgAB6JwhmFBuJU7uSePtc_sAAsnMMRtMKNBIu_FdzmoTAR0BAAMCAAN5AAMwBA"
    )
    await callback.message.answer("<b>Список моделей Omoda:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHAmUamayVrvZCgXg8o9KcCBzJ2ImqAALGzDEbTCjQSHbVj0ckUtPRAQADAgADeQADMAQ",
        caption="Omoda С5",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHBGUambF6GU0xWJ_RqYblsOFaO-WYAALHzDEbTCjQSEQaLjTZTnlFAQADAgADeQADMAQ",
        caption="Omoda S5",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "tank")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Tank:</b>\nОригинальное произношение "Тан Кэ", в переводе - "танк"\nОбычно произносят как "Танк" или "Тэнк"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHE2Uam5ny414ld20kKsJ7eLDrlqoJAALRzDEbTCjQSGn91TRbj-a5AQADAgADeAADMAQ"
    )
    await callback.message.answer("<b>Список моделей Tank:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHFWUam6BiITYWlZsqbumaIZCADsyzAALPzDEbTCjQSH8zU8hs3TWDAQADAgADeQADMAQ",
        caption="Tank 300",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHF2Uam6Xilbl-Re2y1jGLxQihYhAZAALQzDEbTCjQSP-DfuvqcWthAQADAgADeQADMAQ",
        caption="Tank 500",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "vortex")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Vortex:</b>\nВ переводе - "вихрь" или "водоворот"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHLGUanYaOQLYebVXq4YHMDPiT6IEyAALnzDEbTCjQSJ4euGwVXzs2AQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Vortex:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHMGUanZ37BA4yuu3qgtfgNWwd-VS5AALozDEbTCjQSHFNfKnju_0vAQADAgADeAADMAQ",
        caption="Vortex Estina I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHMmUanaOrJb-_DL5BQSHxgHnYML0JAALpzDEbTCjQSLsKblW8_gw8AQADAgADeQADMAQ",
        caption="Vortex Tingo I",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHOGUaoEnLOoUlxN5pwV7F7J67XEDlAAPNMRtMKNBIjEB4YXiApJIBAAMCAAN4AAMwBA",
        caption="Vortex Tingo I (FL)",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "voyah")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Voyah:</b>\nОригинальное произношение "Фэн Ту" или "Во Йя", в переводе - "движение энергии"\nОбычно произносят как "Воя"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHSWUaoTbk1ObLYvputt7EEwpkq7XdAAIGzTEbTCjQSBoI21brZOSQAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Voyah:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHS2UaoT8jBs-lTgitf5vjswE85gAEAs0xG0wo0EjgneWRuPXVCgEAAwIAA3kAAzAE",
        caption="Voyah Dream",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHTWUaoUaL6Roar-XLxQxx8c44fROkAAIEzTEbTCjQSBtp7KjWfrAPAQADAgADeQADMAQ",
        caption="Voyah Free",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHT2UaoUz0MoTpc7ricEJKoM221eoAAwXNMRtMKNBIEWleniyxKE8BAAMCAAN5AAMwBA",
        caption="Voyah Passion",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "zeekr")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Zeekr:</b>\nОбычно произносят как "Зикр"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHamUao8hB6RecNPH2ytK7Avcnhcg0AAIRzTEbTCjQSKcF__95vmiGAQADAgADeQADMAQ"
    )
    await callback.message.answer("<b>Список моделей Zeekr:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHbGUao9D-pJqMu1UlsXw-Ccz3SfrvAAINzTEbTCjQSMMV0C8dUqcJAQADAgADeQADMAQ",
        caption="Zeekr 001",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHbmUao9VKx8fQdmvs9wxOP0-vWZAgAAIPzTEbTCjQSOv2mc89c0iqAQADAgADeQADMAQ",
        caption="Zeekr 009",
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHcGUao9ofMH3Ez7DCc7uLwrKX87gDAAIQzTEbTCjQSOtugl29Ezw9AQADAgADeQADMAQ",
        caption="Zeekr X",
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "zotye")
async def details(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали {callback.data.capitalize()}!")
    await callback.message.answer(
        '<b>Логотип бренда Zotye:</b>\nОбычно произносят как "Зоти"'
    )
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHfmUapOE422HzGukAARpot9-BOsRoigACF80xG0wo0EghzaZ7-p-MawEAAwIAA3kAAzAE"
    )
    await callback.message.answer("<b>Список моделей Zotye:</b>")
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIHgGUapOhV7o3PJylKBccTr0HkqfYRAAIVzTEbTCjQSGAItN0vgzhzAQADAgADeQADMAQ",
        caption="Zotye T600",
    )


@router.message(F.photo)
async def download_photo(message: Message):
    photo = await bot.get_file(message.photo[-1].file_id)
    current_datetime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    photo_name = f"{current_datetime}.jpg"
    photo_path = os.path.join("Pictures", photo_name)
    await bot.download_file(photo.file_path, photo_path)

    detect = yolo_detect(photo_path)
    if detect == 1:
        pred = yolo_results(photo_path)
        await message.answer(pred)
    else:
        await message.answer(
            "Бот 🤖 <b>НЕ РАСПОЗНАЛ</b> ни одного автомобиля 🚘! \n<b>Попробуйте отправить другое фото</b> 📸"
        )


@router.message()
async def echo(message: Message):
    await message.answer(
        "Отправьте фото 📸 АВТОМОБИЛЯ 🚗 данному боту 🤖 или воспользуйтесь встроенными кнопками меню ▶️"
    )
