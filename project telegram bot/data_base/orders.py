import sqlite3 as sq
from aiogram import types
import keyboards_constants as kc
from aiogram.dispatcher.dispatcher import Dispatcher

from config import adminid
from config import dp, bot

from keyboards import admin_a_r,reject

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data_base import sqlite_db

def orders_start():
    global base4, cur4
    base4 = sq.connect('orders.db')
    cur4 = base4.cursor()
    if base4:
        print('Orders Data base is connected OK!')
    base4.execute(
        'CREATE TABLE IF NOT EXISTS menu(id INT,passport TEXT, name TEXT,cars_name TEXT PRIMARY KEY,method_pay TEXT ,is_ordered INT)')
    base4.commit()


async def orders_add_command(id,photos,customer,cars_name,method,is_odered):
    
        cur4.execute('INSERT OR IGNORE INTO menu VALUES (?,?,?,?,?,?)',(id,photos,customer,cars_name,method,is_odered,))
        base4.commit()


async def admin_oreders_read():
    for ret in cur4.execute("SELECT * FROM menu WHERE is_ordered = 1").fetchall():
        await bot.send_photo(adminid,photo=ret[1] ,caption=f"\t📥 You have new order\n\n👤 Customer: {ret[2]}\n\n🚘 Car's name:{ret[3]}\n\n🏦 Payment Method:{ret[4]}",
         reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text=kc.ACCEPT,callback_data=f'accept {ret[3]}'),reject,InlineKeyboardButton(text=kc.BANK_ACCEPT,callback_data='bank')))


async def clients_order(data,message):
    try:
     for ret in cur4.execute("SELECT * FROM menu WHERE name == ? AND is_ordered = 1",(data,)).fetchall():
        
        await bot.send_photo(message.from_user.id,photo=await sqlite_db.car_photo(ret[3]),caption=f"👤 Customer: {ret[2]}\n\n🚘 Car's name: {ret[3]}\n\n💵Price: {await sqlite_db.price(ret[3])} UZS \n\n🏦 Payment Method:{ret[4]}",
         reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=kc.CANCEL_ORDER,callback_data=f'cancel {ret[0]}')))
    except:
        await bot.send_message(message.from_user.id,"You don't any have 📭 order yet")
async def auto_delete():
    cur4.execute("DELETE FROM menu WHERE  id == date('now','-30 day')")
    base4.commit()


async def canceled(data):
    cur4.execute("DELETE FROM menu WHERE id == ?",(data,))
    
    base4.commit()