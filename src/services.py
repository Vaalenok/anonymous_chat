import asyncio
import logging

from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from tenacity import retry, stop_never, retry_if_exception_type, RetryCallState


async def dynamic_wait(retry_state: RetryCallState):
    exception = retry_state.outcome.exception()

    if isinstance(exception, TelegramRetryAfter):
        await asyncio.sleep(exception.retry_after)
    else:
        await asyncio.sleep(1)


@retry(
    stop=stop_never,
    retry=retry_if_exception_type(TelegramRetryAfter),
    before_sleep=dynamic_wait
)
async def message_user(user_id: int, message: str, keyboard=None):
    from bot import bot
    try:
        await bot.send_message(user_id, message, reply_markup=keyboard)
    except TelegramForbiddenError:
        logging.warning(f"Пользователь {user_id} заблокировал бота. Не удалось отправить сообщение")
