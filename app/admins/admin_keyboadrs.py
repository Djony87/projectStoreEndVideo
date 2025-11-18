from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_item_by_category

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

async def admin_keyboards_add_item():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.row(InlineKeyboardButton(text=category.name, callback_data=f'addCategory_{category.id}'))
    return keyboard.as_markup()


async def admin_keyboards_delete_item():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.row(InlineKeyboardButton(text=category.name, callback_data=f'deleteCategory_{category.id}'))
    keyboard.row(InlineKeyboardButton(text='К панели Админ', callback_data='admin'))
    return keyboard.as_markup()

async def admin_keyboards_all_item(category_id):
    get_items = await get_item_by_category(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in get_items:
        keyboard.row(InlineKeyboardButton(text=item.name, callback_data=f'deleteItem_{item.id}'))
    keyboard.row(InlineKeyboardButton(text='К какегориям', callback_data='delete_item'))
    return keyboard.as_markup()


async def admin_delete_keyboard_back(category_id):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data=f'deleteCategory_{category_id}')]])
