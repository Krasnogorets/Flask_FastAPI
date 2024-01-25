"""
Задание

Объедините студентов в команды по 2-5 человек в сессионных залах.

Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары,
заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY),
id товара (FOREIGN KEY), дата заказа и статус заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц
(итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
* Чтение всех
* Чтение одного
* Запись
* Изменение
* Удаление

"""
import datetime
import databases
import pandas as pd
import sqlalchemy
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import create_engine, ForeignKey
from hashlib import sha256
from datetime import datetime
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="hw6/static"), name="static")
templates = Jinja2Templates(directory="hw6/templates")
DATABASE_URL = "sqlite:///new2.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table("users", metadata, sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("secondname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(60)),
                         sqlalchemy.Column("password", sqlalchemy.String(64)))
orders = sqlalchemy.Table("orders", metadata, sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("users.id")),
                          sqlalchemy.Column("goods_id", sqlalchemy.Integer, ForeignKey("goods.id")),
                          sqlalchemy.Column("date", sqlalchemy.TIMESTAMP),
                          sqlalchemy.Column("status", sqlalchemy.String(32)))
goods = sqlalchemy.Table("goods", metadata, sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("title", sqlalchemy.String(32)),
                         sqlalchemy.Column("description", sqlalchemy.String(500)),
                         sqlalchemy.Column("price", sqlalchemy.Float))

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class UserIn(BaseModel):
    name: str = Field(max_length=32, min_length=3)
    secondname: str = Field(max_length=32, min_length=5)
    email: EmailStr = Field(max_length=60)


class User(BaseModel):
    id: int
    name: str = Field(..., max_length=32, min_length=2)
    secondname: str = Field(..., max_length=32, min_length=2)
    email: EmailStr = Field(..., max_length=60)
    password: str = Field(..., max_length=64)


class Orders(BaseModel):
    id: int
    user_id: int
    goods_id: int
    date: datetime
    status: str = Field(..., max_length=32)


class OrdersIn(BaseModel):
    user_id: int
    goods_id: int
    date: datetime
    status: str = Field(..., max_length=32)


class Goods(BaseModel):
    id: int
    title: str = Field(..., max_length=32, min_length=2)
    description: str = Field(default=None, max_length=500)
    price: float = Field(..., gt=0, le=100_000)


class GoodsIn(BaseModel):
    title: str = Field(..., max_length=32, min_length=2)
    description: str = Field(default=None, max_length=500)
    price: float = Field(..., gt=0, le=100_000)


@app.get('/', response_class=HTMLResponse)
async def index():
    return '<h1>проект подготовка для интернет магазина</h1>'


# USERS------------------------------------

# FIRST USERS CREATION------------------------------------
# @app.get("/fake_users/{count}")
# async def create_users(count: int):
#     for i in range(count):
#         query = users.insert().values(name=f'user_{i}', secondname=f'user_user_{i}', email=f'user_{i}@mail.ru',
#                                       password=sha256('123'.encode(encoding='utf-8')).hexdigest())
#         await database.execute(query)
#     return {'message': f'{count} fake users create'}


@app.post("/users/", response_model=UserIn)
async def create_user(user: User):
    query = users.insert().values(name=user.name, secondname=user.secondname, email=user.email,
                                  password=sha256(user.password.encode(encoding='utf-8')).hexdigest())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@app.get("/users/", response_class=HTMLResponse)
async def read_users(request: Request):
    query = users.select()
    task_table = pd.DataFrame([user for user in await database.fetch_all(query)])
    task_table = task_table.loc[:, task_table.columns != 'password']
    task_table.set_index('id', inplace=True)
    return templates.TemplateResponse("users_table.html",
                                      {'request': request,
                                       'table': task_table.to_html(classes='table table-striped text-center',
                                                                   justify='center'),
                                       'table_header': 'Список пользователей: '})


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(user_id: int, request: Request):
    try:
        task_table = pd.DataFrame([await database.fetch_one(users.select().where(users.c.id == user_id))])
        task_table = task_table.loc[:, task_table.columns != 'password']
        task_table.set_index('id', inplace=True)
        return templates.TemplateResponse("users_table.html",
                                          {'request': request,
                                           'table': task_table.to_html(classes='table table-striped text-center',
                                                                       justify='center'),
                                           'table_header': 'Список пользователей: '})
    except:
        return templates.TemplateResponse("not_found.html",
                                          {'request': request, 'id': user_id, 'object': "пользователь"})


@app.put("/users/{user_id}", response_model=UserIn)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}", response_class=HTMLResponse)
async def delete_user(user_id: int, request: Request):
    try:
        task_table = pd.DataFrame([await database.fetch_one(users.select().where(users.c.id == user_id))])
        task_table = task_table.loc[:, task_table.columns != 'password']
        task_table.set_index('id', inplace=True)
        query = users.delete().where(users.c.id == user_id)
        await database.execute(query)
        return templates.TemplateResponse("users_table.html",
                                          {'request': request,
                                           'table': task_table.to_html(classes='table table-striped text-center',
                                                                       justify='center'),
                                           'table_header': 'Удален пользователь: '})
    except:
        return templates.TemplateResponse("not_found.html",
                                          {'request': request, 'id': user_id, 'object': "пользователь"})


# GOODS---------------------------------------------
@app.post("/goods/", response_model=GoodsIn)
async def create_good(good: GoodsIn):
    query = goods.insert().values(title=good.title, description=good.description, price=good.price)
    last_record_id = await database.execute(query)
    return {**good.model_dump(), "id": last_record_id}


@app.get("/goods/", response_class=HTMLResponse)
async def read_goods(request: Request):
    task_table = pd.DataFrame([good for good in await database.fetch_all(goods.select())])
    task_table.set_index('id', inplace=True)
    return templates.TemplateResponse("users_table.html",
                                      {'request': request,
                                       'table': task_table.to_html(classes='table table-striped text-center',
                                                                   justify='center'),
                                       'table_header': 'Список товаров: '})


@app.get("/goods/{good_id}", response_class=HTMLResponse)
async def read_good(good_id: int, request: Request):
    try:
        goods_table = pd.DataFrame([await database.fetch_one(goods.select().where(goods.c.id == good_id))])
        goods_table.set_index('id', inplace=True)
        return templates.TemplateResponse("users_table.html",
                                          {'request': request,
                                           'table': goods_table.to_html(classes='table table-striped text-center',
                                                                        justify='center'),
                                           'table_header': 'Найден товар: '})
    except:
        return templates.TemplateResponse("not_found.html",
                                          {'request': request, 'id': good_id, 'object': "Товар"})


@app.put("/goods/{good_id}", response_model=GoodsIn)
async def update_goods(good_id: int, new_good: GoodsIn):
    query = goods.update().where(goods.c.id == good_id).values(**new_good.model_dump())
    await database.execute(query)
    return {**new_good.model_dump(), "id": good_id}


@app.delete("/goods/{good_id}", response_class=HTMLResponse)
async def delete_good(good_id: int, request: Request):
    try:
        goods_table = pd.DataFrame([await database.fetch_one(goods.select().where(goods.c.id == good_id))])
        goods_table.set_index('id', inplace=True)
        query = goods.delete().where(goods.c.id == good_id)
        await database.execute(query)
        return templates.TemplateResponse("users_table.html",
                                          {'request': request,
                                           'table': goods_table.to_html(classes='table table-striped text-center',
                                                                        justify='center'),
                                           'table_header': 'Удален товар: '})
    except:
        return templates.TemplateResponse("not_found.html",
                                          {'request': request, 'id': good_id, 'object': "Товар"})


# ORDERS---------------------------------------------

@app.post("/orders/", response_model=OrdersIn)
async def create_order(order: OrdersIn):
    query = orders.insert().values(user_id=order.user_id, goods_id=order.goods_id,
                                   date=datetime.now(), status=order.status)
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app.get("/orders/", response_class=HTMLResponse)
async def read_orders(request: Request):
    orders_table = pd.DataFrame([order for order in await database.fetch_all(orders.select())])
    orders_table.set_index('id', inplace=True)
    return templates.TemplateResponse("users_table.html",
                                      {'request': request,
                                       'table': orders_table.to_html(classes='table table-striped text-center',
                                                                     justify='center'),
                                       'table_header': 'Список заказов: '})


@app.get("/orders/{order_id}", response_class=HTMLResponse)
async def read_good(order_id: int, request: Request):
    try:
        orders_table = pd.DataFrame([await database.fetch_one(orders.select().where(orders.c.id == order_id))])
        orders_table.set_index('id', inplace=True)
        return templates.TemplateResponse("users_table.html",
                                          {'request': request,
                                           'table': orders_table.to_html(classes='table table-striped text-center',
                                                                         justify='center'),
                                           'table_header': 'Найден заказ: '})
    except:
        return templates.TemplateResponse("not_found.html",
                                          {'request': request, 'id': order_id, 'object': "Заказ"})


@app.put("/orders/{order_id}", response_model=OrdersIn)
async def update_goods(order_id: int, new_order: OrdersIn):
    query = orders.update().where(orders.c.id == order_id).values(user_id=new_order.user_id, goods_id=new_order.goods_id,
                                   date=datetime.now(), status=new_order.status)
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}", response_class=HTMLResponse)
async def delete_order(order_id: int, request: Request):
    try:
        goods_table = pd.DataFrame([await database.fetch_one(orders.select().where(orders.c.id == order_id))])
        goods_table.set_index('id', inplace=True)
        query = orders.delete().where(orders.c.id == order_id)
        await database.execute(query)
        return templates.TemplateResponse("users_table.html",
                                          {'request': request,
                                           'table': goods_table.to_html(classes='table table-striped text-center',
                                                                        justify='center'),
                                           'table_header': 'Удален заказ: '})
    except:
        return templates.TemplateResponse("not_found.html",
                                          {'request': request, 'id': order_id, 'object': "Заказ"})
