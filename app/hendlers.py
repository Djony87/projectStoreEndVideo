from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboards  as kb
from app.database.requests import (
    set_user, get_item,
    get_added_item_catt,
    user_shopping_cart)

router = Router()

class Reg(StatesGroup):
    tg_id = State()
    user_name = State()
    user_soname = State()
    phone_number = State()


class AddItemCart(StatesGroup):
    id = State()
    tg_id = State()
    item_id = State()


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



@router.callback_query(F.data == 'start')
async def callback_start(callback: CallbackQuery):
    await callback.answer('Вы вернулись на главное меню')
    await callback.message.edit_text(f'Вас приветствует приевествует бот \n'
                                     f'интернет-магазина одежды.',
                                     reply_markup=kb.kb_start)


@router.callback_query(F.data == 'cart')
async def item_in_cart(callback: CallbackQuery):
    await callback.answer('')
    all_items_in_cart = await user_shopping_cart(callback.from_user.id)
    print(all_items_in_cart)
    for item in all_items_in_cart:
        try:
            await callback.message.answer_photo(photo=item[0])
        except:
            pass
        await callback.message.answer(f'{item[1]}\n'
                                      f'{item[2]}')


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите категорию товара',
                                     reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите товар по категории',
                                     reply_markup=await kb.get_items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def item_hendler(callback: CallbackQuery):
    item = await get_item(callback.data.split('_')[1])
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


@router.callback_query(F.data.startswith('cart_'))
async def added_cart(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(AddItemCart.tg_id)
    await state.update_data(tg_id=callback.from_user.id)
    await state.set_state(AddItemCart.item_id)
    await state.update_data(item_id=callback.data.split('_')[1])

    data = await state.get_data()

    await  get_added_item_catt(
        tg_id=data['tg_id'],
        item_id=data['item_id']
    )
    await state.clear()
    await callback.message.answer(f'Товар добавлен в корзину')
