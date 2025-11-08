from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards  as kb
from app.admins.admin_keyboadrs import kb_admin
from app.database.requests import set_user, get_item, get_all_user
from config import ID_ADMIN

router = Router()

class Reg(StatesGroup):
    tg_id = State()
    user_name = State()
    user_soname = State()
    phone_number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'{message.from_user.first_name},\n'
                        f'Вас приветствует приевествует бот \n'
                        f'    интернет-магазина одежды.',
                        reply_markup=kb.kb_start)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f'Это команда help, ваш id: {message.from_user.id}',
                         reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data == 'admin')
async def admin_panel(callback: CallbackQuery):
    id_user = callback.from_user.id
    if id_user in ID_ADMIN:
        await callback.message.edit_text('Вы вошли как администратор',
                                      reply_markup=kb_admin)
    else:
        await callback.message.edit_text('У вас нет доступа к ресурсам')


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


@router.callback_query(F.data == 'reg')
async def add_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Reg.phone_number)
    await callback.message.answer('Для регистрации введите номер телефона')


@router.message(Reg.phone_number)
async def add_user(message: Message, state: FSMContext):
    # Собираем все данные в состояние
    await state.update_data(phone_number=message.text)
    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(user_name=message.from_user.first_name)
    await state.update_data(user_soname=message.from_user.last_name)

    # Получаем данные из состояния с другим именем переменной
    user_data = await state.get_data()

    # Сохраняем пользователя
    await set_user(
        tg_id=user_data['tg_id'],
        user_name=user_data['user_name'],
        user_soname=user_data['user_soname'],
        phone_number=user_data['phone_number']
    )

    await state.clear()
    await message.answer("Регистрация завершена успешно! ✅")
    await state.clear()


@router.callback_query(F.data == 'all_users')
async def all_users(callback: CallbackQuery):
    await callback.answer()
    users = await get_all_user()
    for user in users:
        await callback.message.answer(f'Имя пользователя: {user}')
    await callback.message.answer(f'Всего {len(users)} пользователей')