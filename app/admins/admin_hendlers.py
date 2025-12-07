import os
from os.path import split

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from app.admins.admin_keyboadrs import (kb_admin,
                                        admin_keyboards_add_item,
                                        admin_keyboards_delete_item,
                                        admin_delete_keyboard_back,
                                        admin_keyboards_all_item,
                                        kb_product_addad,
                                        back_button_after_deletion)
from app.database.requests import get_all_user, set_item, get_item, delete_position


admin_router = Router()
load_dotenv()


class AddItem(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    photo = State()
    count = State()





class DeleteState(StatesGroup):
    warning_for_confirmation = State()

@admin_router.message(Command('admin'))
async def admin_panel(message: Message):
    id_user = message.from_user.id
    if id_user in list(map(int, os.getenv('ID_ADMIN', '').split(','))):
        await message.answer('Вы вошли как администратор',
                                      reply_markup=kb_admin)
    else:
        await message.answer('У вас нет доступа к ресурсам')

@admin_router.callback_query(F.data == 'admin')
async def admin_panel(callback: CallbackQuery):
    id_user = callback.from_user.id
    if id_user in list(map(int, os.getenv('ID_ADMIN', '').split(','))):
        await callback.message.answer('Вы вошли как администратор',
                                      reply_markup=kb_admin)
    else:
        await callback.message.answer('У вас нет доступа к ресурсам')


@admin_router.callback_query(F.data == 'all_users')
async def all_users(callback: CallbackQuery):
    await callback.answer()
    users = await get_all_user()
    for user in users:
        await callback.message.answer(f'Имя пользователя: {user}')
    await callback.message.answer(f'Всего {len(users)} пользователей')

# -------хендлеры для добавления нового товара

@admin_router.callback_query(F.data == 'add_item')
async def addition(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AddItem.category)
    await callback.message.answer('Выберите категорию товара',
                                  reply_markup=await admin_keyboards_add_item())

@admin_router.callback_query(F.data.startswith('addCategory_'))
async def add_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[1])
    await state.set_state(AddItem.name)
    await callback.message.answer('Введите наименование товара')

@admin_router.message(AddItem.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddItem.description)
    await message.answer('Введите описание товара')

@admin_router.message(AddItem.description)
async def add_discription(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddItem.price)
    await message.answer('Введите цену товара')

@admin_router.message(AddItem.price)
async def add_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AddItem.photo)
    await message.answer('Вставьте фото')


@admin_router.message(AddItem.photo)
async def add_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[1].file_id)
    await state.set_state(AddItem.count)
    await message.answer('Введите колличество')

@admin_router.message(AddItem.count)
async def add_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)

    iten_data = await state.get_data()

    await set_item(
        category = iten_data['category'],
        name = iten_data['name'],
        description = iten_data['description'],
        price = iten_data['price'],
        photo = iten_data['photo'],
        count = iten_data['count']
    )
    await state.clear()
    await message.answer('Товар добавлен', reply_markup=kb_product_addad)
#-----------------------------------------------------------------


# --------хендлер для удаления товара
@admin_router.callback_query(F.data == 'delete_item')
async def deleteItem(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите категорию товар.',
                                     reply_markup = await admin_keyboards_delete_item())


@admin_router.callback_query(F.data.startswith('deleteCategory_'))
async def one_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text('Выберете товар',
                                     reply_markup= await admin_keyboards_all_item(callback.data.split('_')[1]))
    await state.clear()

@admin_router.callback_query(F.data.startswith('deleteItem_'))
async def two_delete(callback: CallbackQuery, state: FSMContext):
    delete = await get_item(callback.data.split('_')[1])
    await callback.answer('')
    await callback.message.edit_text(f'{delete.name}\n\n{delete.description}\n\nЦена: {delete.price}',
                                     reply_markup = await admin_delete_keyboard_back(delete.category))

    await state.update_data(delete_line = delete.id)


@admin_router.callback_query(F.data == 'delete_position')
async def free_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    data = await state.get_data()
    delete_line = data.get('delete_line')
    index = await get_item(delete_line)
    await delete_position(delete_line)
    await state.clear()
    await callback.message.answer('Удаленно',
                                  reply_markup = await back_button_after_deletion(index.category))
