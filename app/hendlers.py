from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import app.keyboards  as kb
from app.database.requests import set_user, get_item

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id, message.from_user.first_name)
    await message.answer(f'{message.from_user.first_name},\n'
                        f'Вас приветствует приевествует бот \n'
                        f'    интернет-магазина одежды.',
                        reply_markup=kb.kb_start)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Это команда help',
                         reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data == 'start')
async def callback_start(callback: CallbackQuery):
    await callback.answer('Вы вернулись на главное меню')
    await callback.message.edit_text(f'Вас приветствует приевествует бот \n'
                                     f'интернет-магазина одежды.',
                                     reply_markup=kb.kb_start)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберете категорию товара',
                                     reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберете товар по категории',
                                     reply_markup=await kb.get_items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def item_hendler(callback: CallbackQuery):
    item = await get_item(callback.data.split('_')[1])
    print(f'результат-{callback.data.split('_')[1]}___{callback.data.split('_')[0]}')
    await callback.answer('')
    await callback.message.edit_text(f'{item.name}\n\n{item.description}\n\nЦена: {item.price}',
                                  reply_markup=await kb.back_category(item.category))