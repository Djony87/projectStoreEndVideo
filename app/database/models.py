from sqlalchemy import String, BigInteger, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import DB_URL


engine = create_async_engine(url=DB_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ =  'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column()
    user_name: Mapped[str] = mapped_column(String(25))
    user_soname: Mapped[str] = mapped_column(String(25), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25))


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(512))
    price: Mapped[int]


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ------- Добавление новых столбцов в таблицу
# async def add_columns_to_users():
#     async with engine.begin() as conn:
#         await conn.execute(text("""
#             ALTER TABLE users
#             ADD COLUMN user_soname VARCHAR(25)
#         """))
#         await conn.execute(text("""
#             ALTER TABLE users
#             ADD COLUMN phone_number VARCHAR(15)
#         """))