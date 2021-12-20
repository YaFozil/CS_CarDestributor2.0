from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import storage

storage = MemoryStorage()

TOKEN = "5070079969:AAHLRRDK5GpikLFGi-fNrByoc_nzpvFE50Q"
adminid = 1274050037

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
