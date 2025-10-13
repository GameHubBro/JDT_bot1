from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards import main_menu

router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        "Привет! 💫 Я помогу рассчитать стоимость тату, показать галерею и многое другое.",
        reply_markup=main_menu
    )
