"""
Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и
пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и
пароль.
• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY),
                                                    id товара (FOREIGN KEY), дата заказа и статус заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.
"""

from datetime import date
import databases
import sqlalchemy
import uvicorn
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///market.db"

app = FastAPI()

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(50)),
)

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(150)),
    sqlalchemy.Column("description", sqlalchemy.String(1024)),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("good_id", sqlalchemy.ForeignKey('goods.id'), nullable=False),
    sqlalchemy.Column("order_date", sqlalchemy.Date),
    sqlalchemy.Column("status", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=50)


class User(UserIn):
    id: int


class GoodIn(BaseModel):
    name: str = Field(max_length=150)
    description: str = Field(max_length=1024)
    price: float = Field(gt=0)


class Good(GoodIn):
    id: int


class OrderIn(BaseModel):
    user_id: int = Field(gt=0)
    good_id: int = Field(gt=0)
    order_date: date
    status: int = Field(ge=0, le=5)


class Order(OrderIn):
    id: int


# Пользователи
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    record_id = await database.execute(query)
    return {**user.dict(), "id": record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    if await database.execute(query):
        return {**new_user.dict(), "id": user_id}
    else:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    if await database.execute(query):
        return {'message': f'User id={user_id} deleted'}
    else:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')


# Товары
@app.post("/goods/", response_model=Good)
async def create_good(good: GoodIn):
    query = goods.insert().values(name=good.name, description=good.description, price=good.price)
    record_id = await database.execute(query)
    return {**good.dict(), "id": record_id}


@app.get("/goods/", response_model=List[Good])
async def read_goods():
    query = goods.select()
    return await database.fetch_all(query)


@app.get("/goods/{good_id}", response_model=Good)
async def read_good(good_id: int):
    query = goods.select().where(goods.c.id == good_id)
    return await database.fetch_one(query)


@app.put("/goods/{good_id}", response_model=Good)
async def update_good(good_id: int, new_good: GoodIn):
    query = goods.update().where(goods.c.id == good_id).values(**new_good.dict())
    if await database.execute(query):
        return {**new_good.dict(), "id": good_id}
    else:
        raise HTTPException(status_code=404, detail=f'Good {good_id} not found')


@app.delete("/goods/{good_id}")
async def delete_good(good_id: int):
    query = goods.delete().where(goods.c.id == good_id)
    if await database.execute(query):
        return {'message': f'Good id={good_id} deleted'}
    else:
        raise HTTPException(status_code=404, detail=f'Good {good_id} not found')


# Заказы
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = users.select().where(users.c.id == order.user_id)
    if not await database.fetch_one(query):
        raise HTTPException(status_code=404, detail=f'User {order.user_id} not found')
    query = goods.select().where(goods.c.id == order.good_id)
    if not await database.fetch_one(query):
        raise HTTPException(status_code=404, detail=f'Good {order.good_id} not found')

    query = orders.insert().values(user_id=order.user_id, good_id=order.good_id, order_date=order.order_date,
                                   status=order.status)
    record_id = await database.execute(query)
    return {**order.dict(), "id": record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = users.select().where(users.c.id == new_order.user_id)
    if not await database.fetch_one(query):
        raise HTTPException(status_code=404, detail=f'User {new_order.user_id} not found')
    query = goods.select().where(goods.c.id == new_order.good_id)
    if not await database.fetch_one(query):
        raise HTTPException(status_code=404, detail=f'Good {new_order.good_id} not found')

    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    if await database.execute(query):
        return {**new_order.dict(), "id": order_id}
    else:
        raise HTTPException(status_code=404, detail=f'Order {order_id} not found')


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    if await database.execute(query):
        return {'message': f'Order id={order_id} deleted'}
    else:
        raise HTTPException(status_code=404, detail=f'Order {order_id} not found')


if __name__ == "__main__":
    uvicorn.run("home_work:app", host="127.0.0.1", port=8000, reload=True)
