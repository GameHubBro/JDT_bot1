from aiogram import Router, types
import logging

router = Router()
STUDIOS_URL = "https://justdotattoo.ru/studios"

def _is_studios_text(txt: str | None) -> bool:
    if not txt:
        return False
    t = txt.lower().strip()
    t = t.replace("🏢", "").strip()  # убираем эмодзи
    keywords = ("студ", "мастер", "мастера", "сало", "студии и мастера", "студии")
    return any(k in t for k in keywords)

@router.message(lambda message: _is_studios_text(message.text))
async def studios_handler(message: types.Message):
    await state.clear()
    logging.info(f"[studios] handled message from {message.from_user.id}: {message.text!r}")
    await message.answer(
        "Смотри все студии и мастеров здесь:\n" + STUDIOS_URL
    )



