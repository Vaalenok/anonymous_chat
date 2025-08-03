from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

import src.crud as crud
from src.model import User, Status
from src.services import message_user


router = Router()


@router.message(Command("start"))
async def start(msg: Message):
    user = await crud.get_user(msg.from_user.id)

    if not user:
        new_user = User(
            user_id=msg.from_user.id,
            username=msg.from_user.username,
            name=msg.from_user.first_name
        )

        user = await crud.create_user(new_user)

    await msg.answer(f"Привет, {user.name}\n\n(@{user.username}:{user.user_id})")


@router.message(Command("search"))
async def search(msg: Message):
    user = await crud.get_user(msg.from_user.id)

    if user.status == Status.SEARCH:
        await msg.answer("Ты уже в поиске\n\nОстановить поиск - /stop")
        return

    if user.status == Status.CHAT:
        inter_user = await crud.get_user(user.current_chat)

        if inter_user:
            inter_user.current_chat = None
            inter_user.status = Status.WAITING
            await crud.update_user(inter_user)

            await message_user(inter_user.user_id, "Собеседник завершил чат\n\nИскать чат - /search")

        user.current_chat = None
        user.status = Status.SEARCH
        await crud.update_user(user)

        await message_user(user.user_id, "Ты завершил чат\n\nИщу новый...")
        return

    user.status = Status.SEARCH
    await crud.update_user(user)

    await msg.answer("Ищу собеседника...\n\nОстановить поиск - /stop")


@router.message(Command("stop"))
async def stop(msg: Message):
    user = await crud.get_user(msg.from_user.id)

    if user.status == Status.WAITING:
        await msg.answer("Ты не находишься в чате\n\nИскать чат - /search")
        return

    if user.status == Status.SEARCH:
        user.current_chat = None
        user.status = Status.WAITING
        await crud.update_user(user)
        await msg.answer("Ты остановил поиск чата\n\nИскать чат - /search")
        return

    inter_user = await crud.get_user(user.current_chat)

    if inter_user:
        inter_user.current_chat = None
        inter_user.status = Status.WAITING
        await crud.update_user(inter_user)

        await message_user(inter_user.user_id, "Собеседник завершил чат\n\nИскать чат - /search")

    user.current_chat = None
    user.status = Status.WAITING
    await crud.update_user(user)

    await msg.answer("Ты завершил чат\n\nИскать чат - /search")


@router.message(~F.text.startswith("/"))
async def _message(msg: Message):
    user = await crud.get_user(msg.from_user.id)

    if user.status != Status.CHAT:
        await msg.answer("У тебя нет активного чата\n\nИскать чат - /search")
        return

    await message_user(user.current_chat, msg.text)
