from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from project.crying.apps.bot.commands.bot_commands import BaseCommands

if TYPE_CHECKING:
    from ...locales.stubs.ru.stub import TranslatorRunner

router = Router()


@router.message(Command(BaseCommands.START))
@router.message(Text(startswith="«"))
@router.callback_query(Text("start"))
async def start(message: types.Message | types.CallbackQuery, l10n: TranslatorRunner, state: FSMContext):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    # async with chat_action.ChatActionSender(chat_id=message.chat.id, action="record_video"):
    #     await asyncio.sleep(1)
    await message.answer(l10n.start(name=message.from_user.full_name))
