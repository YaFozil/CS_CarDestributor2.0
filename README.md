# CS_CarDestributor2.0

[This Telegram Bot](https://t.me/CSTESTlabBOT) created by students of TTPU Sobirov Abu-Bakr and Yaminjonov Foziljon to handle sales for car destributors
## Instalation Guide

 - [Instalation Guide of Aiogram](https://docs.aiogram.dev/en/latest/install.html)
 - [Quick Start(for beginers)](https://docs.aiogram.dev/en/latest/quick_start.html)
 - [Download Python Here](https://www.python.org/)
 - [Install SQLite browser for DB](https://sqlitebrowser.org/dl/)
 ## AdminID and TOKEN
- AdminID is in config.pу file,  9-line 
```sh
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import storage

storage = MemoryStorage()

TOKEN = "5070079969:AAHLRRDK5GpikLFGi-fNrByoc_nzpvFE50Q" 
adminid =1234567890 #  <== PUT YOUR ADMINID HERE

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
```
- Use this (in config.pу file, 8-line) TOKEN => 5070079969:AAHLRRDK5GpikLFGi-fNrByoc_nzpvFE50Q to run this program, [reason to use only this token](https://core.telegram.org/bots/api/#sending-files) in our program is that file_id uniquely identifies a file, but a file can have different valid file_ids even for the same bot.
 - This is Click(Test) token => 398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065 client.рy file 164-line
```sh
 provider_token="398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065",
``` 
## Run program
You should run bot in tele_bot.py file
```sh
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
```
## Start bot
- First of all, You have to add [this bot](https://t.me/CSTESTlabBOT) to any group and promote to admin
- Then press /start command in the bot. In the group where the bot is admin choose /moderator command from menu (bot will send you "👨‍💻 Hello Admin!" message.). Now You can add new cars to list of cars and contact details.
- After adding cars and ☎️ contact details you can view them as a client(press /start command to be a client)
## Some screenshots of the Bot for Visualization


- [Start](https://drive.google.com/file/d/1PwnGLgpFC2Ot0iwENuAlr7bUZTyYEyaj/view?usp=drivesdk)
- [Register](https://drive.google.com/file/d/1Ps7cUIDId5AfaVHOlCBX84xf2p2LhCYz/view?usp=drivesdk)
- [My orders & Payment](https://drive.google.com/file/d/1QNbHpg8bSuKiZ9bglfPMfuGRz5_j8t34/view)
- [Contact details](https://drive.google.com/file/d/1QzwWIMESnKauL3R872zbGgfg06qGI1vU/view?usp=drivesdk)
- [Buying options](https://drive.google.com/file/d/1QLnq-8dEknDwsS1p0FE6Yym0fQA6VPvA/view)
- [Admin Add ](https://drive.google.com/file/d/1QKnA-0t-aGM4QK0kk2OamODgsLcVDiJV/view)
- [Admin List of Orders](https://drive.google.com/file/d/1QHtT2E6JjRZCUNNzIj2TpKAMrObW9Wad/view)
- [Accept/Reject order](https://drive.google.com/file/d/1QxIIdHooZswtmY21943vQibdCmBiMCgj/view?usp=drivesdk)

## Chevrolet Cars


![Cars](https://media.assets.sincrod.com/websites/content/gmps-frankporth-wi//b2b9d77795a0476597baf705f070cb73_c492x477-1063x456.jpg)
