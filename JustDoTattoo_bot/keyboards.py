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
            KeyboardButton(text="📖 Полезное про тату"),
        ],
    ],
    resize_keyboard=True
)

# --- Клавиатура для раздела “Полезное про тату” ---
articles_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧠 Как выбрать татуировку"),
        ],
        [
            KeyboardButton(text="💧 Уход за татуировкой"),
        ],
        [
            KeyboardButton(text="🕒 Больно ли делать тату"),
        ],
        [
            KeyboardButton(text="🔗 Все статьи на сайте"),
        ],
        [
            KeyboardButton(text="⬅️ Назад в меню"),
        ],
    ],
    resize_keyboard=True
)

# --- Клавиатура для выбора размера тату ---
size_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Маленькая"), KeyboardButton(text="Средняя"), KeyboardButton(text="Большая")]
    ],
    resize_keyboard=True
)

# --- Клавиатура для выбора количества цветов ---
colors_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Черно-белая"), KeyboardButton(text="Цветная")]
    ],
    resize_keyboard=True
)

# --- Клавиатура для выбора стиля тату ---
style_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Минимализм"), KeyboardButton(text="Реализм")],
        [KeyboardButton(text="Графика"), KeyboardButton(text="Надпись")]
    ],
    resize_keyboard=True
)
