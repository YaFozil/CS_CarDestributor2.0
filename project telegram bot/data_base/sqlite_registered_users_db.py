import sqlite3 as sq
from config import bot


def sql_start_registretion():
    global base3, cur3
    base3 = sq.connect('reg_user.db')
    cur3 = base3.cursor()
    if base3:
        print('Data Reg  base is connected OK!')
    base3.execute(
        'CREATE TABLE IF NOT EXISTS menu(user_name TEXT,img TEXT,userid INT PRIMARY KEY)')
    base3.commit()


async def sql_add_command_users(state):
    async with state.proxy() as data:
        cur3.execute('INSERT INTO menu VALUES (?,?,?)', tuple(data.values()))
        base3.commit()


def sql_find_regisrt_id(people_id):
    result = cur3.execute(
        "SELECT * FROM menu  WHERE userid = ?", (people_id,)).fetchall()
    return bool(len(result))


async def u_name(data):
    result = cur3.execute(
        "SELECT user_name FROM menu  WHERE userid = ?", (data,)).fetchone()
    for i in result:   
        return i

async def photo_send(data):
    result = cur3.execute(
        "SELECT img FROM menu  WHERE userid = ?", (data,)).fetchone()
    for i in result:   
        return i        

