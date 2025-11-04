# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Главное меню ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💰 Рассчитать тату"),
            KeyboardButton(text="🎨 Галерея тату"),
        ],
        [
            KeyboardButton(text="🏙️ Студии и мастера"),
            KeyboardButton(text="📚 Полезное про тату"),
        ],
    ],
    resize_keyboard=True
)

# --- Клавиатура для раздела “Полезное про тату” ---
articles_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 Как выбрать татуировку")],
        [KeyboardButton(text="💧 Уход за татуировкой")],
        [KeyboardButton(text="🕒 Больно ли делать тату")],
        [KeyboardButton(text="🔗 Все статьи на сайте")],
        [KeyboardButton(text="⬅️ Назад в меню")],
    ],
    resize_keyboard=True
)

# --- Клавиатура для выбора размера тату ---
size_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="до 3см"), KeyboardButton(text="от 5см")],
        [KeyboardButton(text="до 7см"), KeyboardButton(text="до 10см")],
        [KeyboardButton(text="до 15см"), KeyboardButton(text="от 15см")],
    ],
    resize_keyboard=True
)

# --- Клавиатура для выбора количества цветов ---
colors_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="один цвет")],
        [KeyboardButton(text="2 цвета")],
        [KeyboardButton(text="3 и больше цветов")],
    ],
    resize_keyboard=True
)

# --- Клавиатура для выбора стиля тату ---
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
