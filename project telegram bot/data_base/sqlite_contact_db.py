from os import readlink
import sqlite3 as sq

from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from config import dp, bot

import keyboards_constants as kc

def sql_start_contact_d():
    global base2, cur2
    base2 = sq.connect('contact_detail.db')
    cur2 = base2.cursor()
    if base2:
        print('Data Contact base is connected OK!')
    base2.execute(
        'CREATE TABLE IF NOT EXISTS menu(location TEXT PRIMARY KEY,address TEXT, phone_number TEXT, email TEXT)')
    base2.commit()


async def sql_add_command_contact(state):
    async with state.proxy() as data:
        cur2.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        base2.commit()


async def sql_read_contact(message):
    for ret in cur2.execute('SELECT * FROM menu').fetchall():
        await bot.send_message(message.from_user.id, f'🗺 Address:  {ret[1]}\n\n📞 Phone number:  {ret[2]}\n\n📧 E-mail:   {ret[-1]}',
        reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=kc.LOCATION,url=ret[0])))


async def get_phone_number():
    phone = cur2.execute('SELECT phone_number FROM menu').fetchall()
    return phone


async def open_map():
    map = cur2.execute('SELECT location FROM menu').fetchall()
    return map
