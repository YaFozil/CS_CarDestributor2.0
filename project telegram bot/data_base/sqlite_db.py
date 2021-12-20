import asyncio
import sqlite3 as sq


from config import dp, bot

from keyboards import admin_a_r

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import keyboards_constants as kc

def sql_start():
    global base, cur
    base = sq.connect('car_cool.db')
    cur = base.cursor()
    if base:
        print('Data base is connected OK!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS menu(img TEXT,name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):

    for ret in cur.execute("SELECT * FROM menu WHERE name == ?",(message.text,)).fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'🚗 Model:  {ret[1]}\n📝 Description:  {ret[2]}\n💸 Price:   {ret[-1]} UZS', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=f"{kc.BUY_BUTTON} {ret[1]}", callback_data=f'Buy {ret[1]}')))


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_read3(data):
    return cur.execute('SELECT * FROM menu WHERE name == ?',(data,)).fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE  FROM menu WHERE name == ?', (data,))
    base.commit()

adminid = 2126572299


async def car_sell(data):
    name = cur.execute(
        'SELECT name FROM menu WHERE name == ?', (data,)).fetchone()
    for i in name:    
        return i

async def car_photo(data):
    for a in cur.execute('SELECT img FROM menu WHERE name == ?',(data,)).fetchone():
      return a

             

async def price(data):
   for i in cur.execute("SELECT price FROM menu WHERE name == ?",(data,)).fetchone():
        return i    