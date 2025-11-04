from aiogram import Router, types
from config import BASE_URL
from config import IDEAS_URL
from logger_utils import log_user_action

router = Router()

@router.message(lambda m: m.text == "🎨 Галерея тату")
async def gallery(message: types.Message):
    await state.clear() 
    log_user_action(message.from_user.id, message.from_user.username, "Перешёл в Галерею")
    await message.answer(
        f'Посмотри крутые работы наших мастеров 👇\n{BASE_URL}/gallery\n'
        f'И подписывайся на наш канал "Тату идеи" 👇\n{IDEAS_URL}'
    )






