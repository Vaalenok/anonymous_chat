import asyncio
import random

import src.crud as crud
from src.model import Status
from src.services import message_user


async def find_inters():
    await asyncio.sleep(5)

    while True:
        await asyncio.sleep(1)

        users = await crud.get_searching_users()

        if len(users) > 1:
            user1, user2 = random.sample(users, 2)

            user1.status = Status.CHAT
            user2.status = Status.CHAT
            user1.current_chat, user2.current_chat = user2.user_id, user1.user_id

            await crud.update_user(user1)
            await crud.update_user(user2)

            await message_user(user1.user_id, "Собеседник найден!")
            await message_user(user2.user_id, "Собеседник найден!")
