from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories




kb_admin = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Добавить товар', callback_data='add_item'),
        InlineKeyboardButton(text='Удалить товар', callback_data='delete_item')],
    [
        InlineKeyboardButton(text='Изменить товар', callback_data='change_item'),
        InlineKeyboardButton(text='Все пользователи', callback_data='all_users')],
    [
        InlineKeyboardButton(text='Назад', callback_data='start')
    ]
])

async def admin_categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.row(InlineKeyboardButton(text=category.name, callback_data=f'addCategory_{category.id}'))
    return keyboard.as_markup()