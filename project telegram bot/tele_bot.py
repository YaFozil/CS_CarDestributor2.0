from aiogram.utils import executor
from config import dp
from data_base import orders, sqlite_contact_db, sqlite_db, sqlite_registered_users_db

from handlers import client, admin


async def on_startup(_):
    print('BOT is online!')
    sqlite_db.sql_start()
    sqlite_contact_db.sql_start_contact_d()
    sqlite_registered_users_db.sql_start_registretion()
    orders.orders_start()
   

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
admin.register_handlers_admin_contacts(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
