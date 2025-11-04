# handlers/calc_tattoo.py
from aiogram import Router
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.input_file import FSInputFile
from math import ceil

router = Router()

# --- Состояния ---
class TattooCalc(StatesGroup):
    waiting_for_style = State()
    waiting_for_size = State()
    waiting_for_colors = State()

# --- Клавиатуры (можешь импортировать из keyboards.py, но для независимости дублирую тексты) ---
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
        [KeyboardButton(text="🎨 Галерея тату"), KeyboardButton(text="🏙️ Студии и мастера")],
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
@router.message(lambda m: m.text and m.text.strip() == "💰 Рассчитать тату")
async def start_calc(message: types.Message, state: FSMContext):
    await state.clear()
    photo = FSInputFile("images/style_example.jpg")
    await message.answer_photo(photo, caption="🎨 Выберите стиль татуировки:", reply_markup=style_kb)
    await state.set_state(TattooCalc.waiting_for_style)


@router.message(TattooCalc.waiting_for_style)
async def choose_style(message: types.Message, state: FSMContext):
    text = (message.text or "").strip()

    # Если пользователь нажал одну из кнопок главного меню — прерываем расчёт и делегируем
    if text in ("🎨 Галерея тату", "📚 Полезное про тату", "🏙️ Студии и мастера", "💰 Рассчитать тату"):
        # Сбрасываем своё состояние
        await state.clear()
        # импортируем соответствующий модуль локально и вызываем его хендлер
        if text == "🎨 Галерея тату":
            from handlers import gallery as gallery_mod
            await gallery_mod.gallery(message, state)
            return
        if text == "📚 Полезное про тату":
            from handlers import articles as articles_mod
            await articles_mod.articles_from_menu(message, state)
            return
        if text == "🏙️ Студии и мастера":
            from handlers import studios as studios_mod
            # studios handler expects message only; call with state to be safe
            await studios_mod.studios_handler(message, state)
            return
        if text == "💰 Рассчитать тату":
            # уже в калькуляторе — перезапустим
            await start_calc(message, state)
            return

    # обычная логика выбора стиля
    style = text
    if style not in STYLE_COEFF:
        await message.answer("Выберите стиль из списка ⬆️")
        return
    await state.update_data(style=style)

    photo = FSInputFile("images/size_example.jpg")
    await message.answer_photo(photo, caption="📏 Выберите примерный размер тату:", reply_markup=size_kb)
    await state.set_state(TattooCalc.waiting_for_size)


@router.message(TattooCalc.waiting_for_size)
async def choose_size(message: types.Message, state: FSMContext):
    text = (message.text or "").strip()

    # защититься от нажатий меню тоже (аналогично)
    if text in ("🎨 Галерея тату", "📚 Полезное про тату", "🏙️ Студии и мастера", "💰 Рассчитать тату"):
        await state.clear()
        if text == "🎨 Галерея тату":
            from handlers import gallery as gallery_mod
            await gallery_mod.gallery(message, state)
            return
        if text == "📚 Полезное про тату":
            from handlers import articles as articles_mod
            await articles_mod.articles_from_menu(message, state)
            return
        if text == "🏙️ Студии и мастера":
            from handlers import studios as studios_mod
            await studios_mod.studios_handler(message, state)
            return
        if text == "💰 Рассчитать тату":
            await start_calc(message, state)
            return

    size = text
    if size not in SIZE_COEFF:
        await message.answer("Выберите размер из списка ⬆️")
        return
    await state.update_data(size=size)

    photo = FSInputFile("images/color_example.jpg")
    await message.answer_photo(photo, caption="🌈 Сколько будет цветов в тату?", reply_markup=colors_kb)
    await state.set_state(TattooCalc.waiting_for_colors)


@router.message(TattooCalc.waiting_for_colors)
async def choose_colors(message: types.Message, state: FSMContext):
    text = (message.text or "").strip()

    # тоже обработаем переход в меню
    if text in ("🎨 Галерея тату", "📚 Полезное про тату", "🏙️ Студии и мастера", "💰 Рассчитать тату"):
        await state.clear()
        if text == "🎨 Галерея тату":
            from handlers import gallery as gallery_mod
            await gallery_mod.gallery(message, state)
            return
        if text == "📚 Полезное про тату":
            from handlers import articles as articles_mod
            await articles_mod.articles_from_menu(message, state)
            return
        if text == "🏙️ Студии и мастера":
            from handlers import studios as studios_mod
            await studios_mod.studios_handler(message, state)
            return
        if text == "💰 Рассчитать тату":
            await start_calc(message, state)
            return

    colors = text
    if colors not in COLOR_COEFF:
        await message.answer("Выберите вариант из списка ⬆️")
        return

    await state.update_data(colors=colors)
    data = await state.get_data()
    style = data["style"]
    size = data["size"]
    colors = data["colors"]

    # --- Расчёт стоимости ---
    price = BASE_PRICE * STYLE_COEFF[style] * SIZE_COEFF[size] * COLOR_COEFF[colors]
    price = int(ceil(price / 500.0) * 500)

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

# --- Повторный расчёт ---
@router.message(lambda m: m.text and m.text.strip() == "💰 Рассчитать снова")
async def recalc(message: types.Message, state: FSMContext):
    await start_calc(message, state)


# --- Оформление заказа ---
@router.message(lambda m: m.text and m.text.strip() == "🖊 Сделать тату")
async def make_order(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Чтобы оформить заказ, перейди по ссылке 👇\n"
        "https://justdotattoo.ru/order/\n\n"
        "или просто отправь сюда фото зоны, где хочешь тату, и мы поможем подобрать мастера 🔥"
    )



