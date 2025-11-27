from itertools import count

from app.database.models import async_session, User, Item, Category
from sqlalchemy import select, update, delete

async def set_user(tg_id: int, user_name: str, user_soname: str, phone_number: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id,
                             user_name = user_name,
                             user_soname = user_soname,
                             phone_number = phone_number))
            await session.commit()
#-------Функция-запрос добавления в нового товара в базу данных
async def set_item(category: int, name: str, description: str, price: int, photo: str, count: str):
    async with async_session() as session:

        # Проверяем, существует ли уже такой товар
        item = await session.scalar(select(Item).where(Item.name == name and Item.price == price))

        if not item:
            # Создаем объект Item и передаем параметры в конструктор
            new_item = Item(
                category=category,
                name=name,
                description=description,
                price=price,
                photo=photo,
                count=count
            )
            session.add(new_item)
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_item_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))

async def get_all_user():
    async with async_session() as session:
        result =  await session.scalars(select(User.user_name))
        return result.all()


async def delete_position(item_id):
    async with async_session() as session:
        stmt = delete(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        await session.commit()  # Теперь коммит работает
        return result.rowcount > 0

