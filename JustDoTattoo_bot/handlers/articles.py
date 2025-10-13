from aiogram import Router, types
from config import ARTICLE_1_URL, ARTICLE_2_URL, ARTICLE_3_URL, ARTICLE_4_URL, ARTICLE_5_URL, ARTICLES_URL
from logger_utils import log_user_action

router = Router()

@router.message(lambda m: m.text == "📚 Полезное про тату")
async def articles(message: types.Message):
    log_user_action(message.from_user.id, message.from_user.username, "Перешёл в статьи")
    await message.answer(
        "Популярные статьи:\n"
        f"<a href='{ARTICLE_1_URL}'>Стоит ли делать татуировку?</a>\n"
        f"<a href='{ARTICLE_2_URL}'>Идеальные зоны для мужской татуировки</a>\n"
        f"<a href='{ARTICLE_3_URL}'>Первая татуировка</a>\n"
        f"<a href='{ARTICLE_4_URL}'>Татуировки и карьера</a>\n"
        f"<a href='{ARTICLE_5_URL}'>Сколько часов уходит на создание тату</a>\n\n"
        f"Много статей на другие темы: <a href='{ARTICLES_URL}'>ссылка</a>",
        parse_mode="HTML"
    )
