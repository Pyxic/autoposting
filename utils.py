from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from tortoise.exceptions import DoesNotExist

import models
from keyboards import chat_callback
from loader import bot
from models import Chat, MessageQueue
from settings import admin_id


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Начало"),
        # types.BotCommand("help", "Помощь"),
        types.BotCommand("admin", "Админ-панель")
    ])


async def add_chat(chat: types.Chat):
    has_chat = await Chat.get_or_none(id=chat.id)
    if has_chat is None:
        invite_link = chat.invite_link
        title = chat.title
        type_of_chat = chat.type
        await Chat.create(id=chat.id,
                          invite_link=invite_link,
                          type=type_of_chat,
                          title=title)
        return 'Чат успешно добавлен'
    else:
        return 'Чат уже есть в списке'


async def delete_chat(chat: int):
    try:
        await Chat.filter(id=chat).delete()
        return "Чат удален!"
    except:
        return "Чат не найден!"


async def get_all_chats_links():
    chats = await Chat.all()
    links = []
    print(chats)
    if len(chats) != 0:
        for chat in chats:
            links.append([chat.title, chat.invite_link])
        return '\n\n'.join(' - '.join(map(str, row)) for row in links)
    return 'Чатов не найдено'


async def generate_inline_keyboard():
    chats = await Chat.all()
    if len(chats) == 0:
        return None
    generated_menu = InlineKeyboardMarkup(row_width=2)
    for chat in chats:
        generated_menu.insert(InlineKeyboardButton(text=chat.title, callback_data=chat_callback.new(chat_id=chat.id)))
    return generated_menu


async def push_message(chat: int):
    chat = await Chat.get_or_none(id=chat)
    if chat is not None:
        message = await MessageQueue.filter(chat_id=chat.id).first()
        if message is None:
            return
        await bot.send_message(chat.id, message.text)
        await MessageQueue.filter(id=message.id).delete()
        return await send_to_admin(f"Бот сделал пост в {chat.title}")
    else:
        return await send_to_admin(f"Бот пытался сделать пост, но чат не был найден")


async def send_to_admin(message: str):
    for admin in admin_id:
        return await bot.send_message(admin, message)


async def get_frequency(call: CallbackQuery, type_frequency: str):
    type_frequency_list = {
        'by_period': 'Введите период частоты постинга в формате "число:тип времени. "'
                     'тип времени [секунда, минута, час]',
        'by_day': 'Введите номер дня в который делать постинг',
        'by_time': 'Введите время, в которое необходимо делать постинг в формате ЧЧ:ММ',
    }
    await call.message.answer(type_frequency_list[type_frequency])

