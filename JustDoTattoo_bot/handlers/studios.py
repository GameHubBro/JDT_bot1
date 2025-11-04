# handlers/studios.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
import logging
import re

router = Router()
STUDIOS_URL = "https://justdotattoo.ru/studios"

def _is_studios_text(txt: str | None) -> bool:
    if not txt:
        return False
    # убираем эмодзи и прочие символы, оставляем буквы/пробелы
    t = txt.lower().strip()
    # удалить все не-буквенно-пробельные символы
    t_clean = re.sub(r"[^а-яa-z0-9\s]", " ", t)
    keywords = ("студ", "мастер", "мастера", "сало", "студии и мастера", "студии")
    return any(k in t_clean for k in keywords)

@router.message(lambda message: _is_studios_text(message.text))
async def studios_handler(message: types.Message, state: FSMContext):
    await state.clear()
    logging.info(f"[studios] handled message from {message.from_user.id}: {message.text!r}")
    await message.answer(
        "Смотри все студии и мастеров здесь:\n" + STUDIOS_URL
    )
