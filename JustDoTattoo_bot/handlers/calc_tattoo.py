from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.input_file import FSInputFile
from math import ceil

from logger_utils import log_user_action  # если не нужен лог, можно убрать

router = Router()

# --- Состояния ---
class TattooCalc(StatesGroup):
    waiting_for_style = State()
    waiting_for_size = State()
    waiting_for_colors = State()

# --- Клавиатуры ---
style_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Не знаю")],
        [KeyboardButton(text="Надпись"), KeyboardButton(text="Графика")],
        [KeyboardButton(text="Геометрия"), KeyboardButton(text="Абстракция")],
        [KeyboardButton(text="Реализм"), KeyboardButton(text="Тонкие линии")],
        [KeyboardButton(text="Блэкворк"), KeyboardButton(text="New School")],
    ],
    resize_keyboard=True
)

size_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="до 3см"), KeyboardButton(text="от 5см")],
        [KeyboardButton(text="до 7см"), KeyboardButton(text="до 10см")],
        [KeyboardButton(text="до 15см"), KeyboardButton(text="от 15см")],
    ],
    resize_keyboard=True
)

colors_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="один цвет")],
        [KeyboardButton(text="2 цвета")],
        [KeyboardButton(text="3 и больше цветов")],
    ],
    resize_keyboard=True
)

final_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Рассчитать снова"), KeyboardButton(text="🖊 Сделать тату")],
        [KeyboardButton(text="🎨 Галерея тату"), KeyboardButton(text="🏢 Студии и мастера")],
        [KeyboardButton(text="📚 Полезное про тату")],
    ],
    resize_keyboard=True
)

# --- Коэффициенты ---
STYLE_COEFF = {
    "Не знаю": 1.0,
    "Надпись": 0.8,
    "Графика": 1.1,
    "Геометрия": 1.2,
    "Абстракция": 1.3,
    "Реализм": 1.6,
    "Тонкие линии": 1.2,
    "Блэкворк": 1.4,
    "New School": 1.5,
}

SIZE_COEFF = {
    "до 3см": 1.0,
    "от 5см": 1.3,
    "до 7см": 1.6,
    "до 10см": 2.0,
    "до 15см": 2.5,
    "от 15см": 3.0,
}

COLOR_COEFF = {
    "один цвет": 1.0,
    "2 цвета": 1.2,
    "3 и больше цветов": 1.5,
}

BASE_PRICE = 3000  # базовая цена

# --- Обработчики ---
@router.message(F.text == "💰 Рассчитать тату")
async def start_calc(message: types.Message, state: FSMContext):
    await state.clear()
    # log_user_action(message.from_user.id, message.from_user.username, "Запустил калькулятор тату")
    photo = FSInputFile("images/style_example.jpg")
    await message.answer_photo(photo, caption="🎨 Выберите стиль татуировки:", reply_markup=style_kb)
    await state.set_state(TattooCalc.waiting_for_style)

@router.message(TattooCalc.waiting_for_style)
async def choose_style(message: types.Message, state: FSMContext):
    style = message.text.strip()
    if style not in STYLE_COEFF:
        await message.answer("Выберите стиль из списка ⬆️")
        return
    await state.update_data(style=style)
    # log_user_action(message.from_user.id, message.from_user.username, f"Выбрал стиль: {style}")
    photo = FSInputFile("images/size_example.jpg")
    await message.answer_photo(photo, caption="📏 Выберите примерный размер тату:", reply_markup=size_kb)
    await state.set_state(TattooCalc.waiting_for_size)

@router.message(TattooCalc.waiting_for_size)
async def choose_size(message: types.Message, state: FSMContext):
    size = message.text.strip()
    if size not in SIZE_COEFF:
        await message.answer("Выберите размер из списка ⬆️")
        return
    await state.update_data(size=size)
    # log_user_action(message.from_user.id, message.from_user.username, f"Выбрал размер: {size}")
    photo = FSInputFile("images/color_example.jpg")
    await message.answer_photo(photo, caption="🌈 Сколько будет цветов в тату?", reply_markup=colors_kb)
    await state.set_state(TattooCalc.waiting_for_colors)

@router.message(TattooCalc.waiting_for_colors)
async def choose_colors(message: types.Message, state: FSMContext):
    colors = message.text.strip()
    if colors not in COLOR_COEFF:
        await message.answer("Выберите вариант из списка ⬆️")
        return
    await state.update_data(colors=colors)
    # log_user_action(message.from_user.id, message.from_user.username, f"Выбрал цвета: {colors}")

    data = await state.get_data()
    style = data["style"]
    size = data["size"]
    colors = data["colors"]

    price = BASE_PRICE * STYLE_COEFF[style] * SIZE_COEFF[size] * COLOR_COEFF[colors]
    price = int(ceil(price / 500.0) * 500)  # округление до 500 вверх

    await message.answer(
        f"✅ Предварительный расчёт:\n\n"
        f"🎨 Стиль: {style}\n"
        f"📏 Размер: {size}\n"
        f"🌈 Цветов: {colors}\n\n"
        f"💰 Примерная стоимость: <b>{price:,} руб.</b>\n\n"
        f"Перейдите по ссылке для оформления заказа: https://justdotattoo.ru/order/ 🔥"
        f"Реальные студии предложат вам свои услуги и точную стоимость",
        parse_mode="HTML",
        reply_markup=final_kb
    )
    await state.clear()


# --- Обработка финальных кнопок ---
@router.message(F.text == "💰 Рассчитать снова")
async def restart_calc(message: types.Message, state: FSMContext):
    await start_calc(message, state)

@router.message(F.text == "🖊 Сделать тату")
async def make_tattoo(message: types.Message):
    await message.answer("Перейдите по ссылке для оформления заказа: https://justdotattoo.ru/order/")

