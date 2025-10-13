import logging

# Логируем в файл user_activity.log
logging.basicConfig(
    filename="user_activity.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

def log_user_action(user_id: int, username: str, action: str):
    logging.info(f"User {user_id} (@{username}): {action}")
