from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.admins.admin_keyboadrs import kb_admin, admin_categories
from app.database.requests import get_all_user, set_item
from config import ID_ADMIN


admin_router = Router()


class AddItem(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    photo = State()


@admin_router.callback_query(F.data == 'admin')
async def admin_panel(callback: CallbackQuery):
    id_user = callback.from_user.id
    if id_user in ID_ADMIN:
        await callback.message.edit_text('Вы вошли как администратор',
                                      reply_markup=kb_admin)
    else:
        await callback.message.edit_text('У вас нет доступа к ресурсам')


@admin_router.callback_query(F.data == 'all_users')
async def all_users(callback: CallbackQuery):
    await callback.answer()
    users = await get_all_user()
    for user in users:
        await callback.message.answer(f'Имя пользователя: {user}')
    await callback.message.answer(f'Всего {len(users)} пользователей')

# -------хендлеры для доавления нового товара

@admin_router.callback_query(F.data == 'add_item')
async def addition(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AddItem.category)
    await callback.message.answer('Выберите категорию товара',
                                  reply_markup=await admin_categories())

@admin_router.callback_query(F.data.startswith('addCategory_'))
async def add_categori(callback: CallbackQuery, state: FSMContext):
    print(callback.data.split('_')[1])
    await state.update_data(category=callback.data.split('_')[1])
    await state.set_state(AddItem.name)
    await callback.message.answer('Введите наименование товара')

@admin_router.message(AddItem.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddItem.description)
    await message.answer('Введите описание товара')

@admin_router.message(AddItem.description)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddItem.price)
    await message.answer('Введите цену товара')

@admin_router.message(AddItem.price)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AddItem.photo)
    await message.answer('Вставьте фото')

@admin_router.message(AddItem.photo)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[1].file_id)

    iten_data = await state.get_data()

    await set_item(
        category = iten_data['category'],
        name = iten_data['name'],
        description = iten_data['description'],
        price = iten_data['price'],
        photo = iten_data['photo']
    )
    await state.clear()
