# handlers/gallery.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from config import BASE_URL, IDEAS_URL
from logger_utils import log_user_action

router = Router()

@router.message(lambda m: m.text and "галерея" in m.text.lower())
async def gallery(message: types.Message, state: FSMContext):
    # Сбрасываем состояние, если пользователь был в калькуляторе
    await state.clear()

    log_user_action(message.from_user.id, message.from_user.username, "Перешёл в Галерею")
    await message.answer(
        f'Посмотри крутые <a href="{BASE_URL}/gallery">работы наших мастеров</a> 💫\n\n'
        f'И подписывайся на наш <a href="{IDEAS_URL}">канал «Тату идеи»</a> 💫'
    )

