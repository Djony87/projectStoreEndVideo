from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

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