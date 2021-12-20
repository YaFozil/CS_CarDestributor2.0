from typing import Text, Union
from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, message
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from config import dp, bot
from keyboards import menu, phone_number, admin_a_r, registration, back_button
from data_base import sqlite_contact_db, sqlite_db, orders
from data_base import sqlite_registered_users_db as user_reg
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
#import keyboards.client_keyboards as kb
from config import adminid
import keyboards_constants as kc
from random import randint







class FSMClient_reg(StatesGroup):
    users_name = State()
    passport = State()
    userid = State()


# @dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state=FSMContext):
    await orders.auto_delete()
    await bot.send_message(message.from_user.id, f"Hi <b>{message.from_user.full_name}</b>! Welcome to ChevroletBot🚗", reply_markup=menu, parse_mode='HTML')
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEDcSJhsafdtfY_LsVl01PGj8sUbAGGtwACAQEAAladvQoivp8OuMLmNCME")


# @dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
 await bot.send_message(message.from_user.id, "🆘 Administrators 👨‍💻 will contact you as soon as possible", reply_markup=phone_number)
    

async def contact_details(message: types.Message):
    await sqlite_contact_db.sql_read_contact(message)
    await bot.send_message(message.from_user.id, "If you have any question contact with @AvtoServiseBot 🆘 Then our administrators 👨‍💻 will contact you as soon as possible")









async def cm_start_registraion_client(message: types.Message):
    await FSMClient_reg.users_name.set()
    await bot.send_message(message.from_user.id,"Enter your full name please",reply_markup=ReplyKeyboardRemove())

async def cancel_reg(message: types.Message):
        await message.reply('✅ Process is canceled successfully',reply_markup=menu)

async def load_users_name(message: types.Message, state=FSMContext):

    async with state.proxy() as data3:
        data3['users_name'] = message.text
    await FSMClient_reg.next()
    await message.answer('🆔 Upload passport or ID card photo')

async def load_passport(message: Union[types.CallbackQuery, types.Message], state=FSMContext, **kwargs):
    async with state.proxy() as data3:
        data3['passport'] = message.photo[0].file_id
        data3['userid'] = message.from_user.id
    await user_reg.sql_add_command_users(state)
    await state.finish()
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEDchphsjc_V7nejrL3U34ZV6F-BbpyHQACSQIAAladvQoqlwydCFMhDiME")
    await message.delete()
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEDcSRhsal4b25XWdrS8AzTVsiky4MPVwACSgIAAladvQrJasZoYBh68CME")
    await message.answer("✅ Successfully registered. You may buy now.", reply_markup=menu)
    



car_lists = []
car_lists = ReplyKeyboardMarkup(resize_keyboard=True).add(back_button)
car_list = []


async def cars_name(message: types.Message):
    read = await sqlite_db.sql_read2()
    for ret in read:
        if ret[1] not in car_list:
            car_list.append(ret[1])
            car_lists.insert(KeyboardButton(ret[1]))

    await bot.send_photo(message.from_user.id, photo='AgACAgIAAxkBAAIRwmGzlpSF8V2_Bz5qVXM66-DX--Y9AAKQujEbxXuZSfA9YcCgIGT3AQADAgADcwADIwQ',
                         caption='List of Chevrolet cars 👇',
                         reply_markup=car_lists)


async def cars2(message: types.Message):
    await sqlite_db.sql_read(message)


async def car_menu_command(message: types.Message):
    await bot.send_photo(message.from_user.id, photo='AgACAgIAAxkBAAIRwmGzlpSF8V2_Bz5qVXM66-DX--Y9AAKQujEbxXuZSfA9YcCgIGT3AQADAgADcwADIwQ', caption='List of Chevrolet cars 👇')
    await sqlite_db.sql_read(message)




async def choice(callback: types.CallbackQuery):
    viabank  = InlineKeyboardButton(text=kc.VIA_BANK,callback_data=f"Via Bank {callback.data.replace('Buy ', '')}")
    await callback.message.answer("Buying options: ",
     reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text=kc.VIA_CLICK,callback_data=f"Via Click {callback.data.replace('Buy ', '')}"),viabank))
    
    
    await callback.answer() 
    
    







async def back(message:types.Message):
    await message.answer("Main menu",reply_markup=menu)
    await message.delete()


async def send_to_admin(callback: types.CallbackQuery):
    global iduser
    iduser = callback.from_user.id
    is_odered = 0
    if user_reg.sql_find_regisrt_id(callback.from_user.id):
        product_id = randint(10**4,10**5)
        pos2 = callback.data.rfind(' ') 
        pos1 = callback.data.find(' ')
        customer = await user_reg.u_name(callback.from_user.id)
        cars_name = callback.data[pos2:].replace(' ','')
        photos = await user_reg.photo_send(callback.from_user.id)
        method = callback.data[pos1:pos2]
        is_odered = 1
        await orders.orders_add_command(product_id,photos,customer,cars_name,method,is_odered)
        await bot.send_message(adminid,"You have 🆕 order. Please check list of orders")
        
        await callback.answer()
        product_id = None
        await bot.send_sticker(callback.from_user.id, sticker="CAACAgIAAxkBAAEDc_xhszDuE4890X2mAknFNOfCw-fq7gACSAIAAladvQoc9XL43CkU0CME")

        await bot.send_message(callback.from_user.id, 'Your order sent to administrators, please wait....')
    if not user_reg.sql_find_regisrt_id(callback.from_user.id):
        await callback.answer("To purchase the car on our bot you should register with 🆔.It takes little time.", show_alert=True)
        await bot.send_message(callback.from_user.id, "Please register...", reply_markup=registration)



async def click(callback: types.CallbackQuery):
    read3 = await sqlite_db.sql_read3(callback.data.replace('accept ', ''))
    await bot.send_message(iduser,"You order accepted please 👇")
    for row in read3:
        await bot.send_invoice(iduser,
                               title=row[1],
                               description=row[2],
                               provider_token="398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065",
                               currency="UZS",
                               prices=[types.LabeledPrice(
                                   label="Click2",
                                   amount=row[3].replace(' ', ''))],
                               start_parameter="Click3",
                               
                               payload="Click4")
    await callback.answer()                           


async def myorder(message: types.Message):
    customer1 = await user_reg.u_name(message.from_user.id)
    await orders.clients_order(customer1,message)

async def cancel_order(callback: types.CallbackQuery):
    await orders.canceled(callback.data.replace('cancel ', ''))
    await bot.send_message(callback.from_user.id,'Your order successfully canceled')
    await callback.answer()
    





# REGISTERING MESSAGE AND CALLBACK HANDLERS TO EXPORT TO TELE_BOT.PY
def register_handlers_client(dp: Dispatcher):
    
    dp.register_message_handler(process_start_command, commands=['start'])
    
    dp.register_message_handler(
        cars_name, lambda message: kc.LIST_OF_CARS in message.text)
    
    dp.register_message_handler(cm_start_registraion_client, lambda message: kc.REGISTER == message.text, state=None)

    dp.register_message_handler(cancel_reg,lambda message: kc.CANCEL_REG == message.text)

    dp.register_message_handler(
        load_users_name, state=FSMClient_reg.users_name)

       

    dp.register_message_handler(load_passport, content_types=[
                                'photo'], state=FSMClient_reg.passport)

                             

    dp.register_message_handler(process_help_command, commands=['help'])

    dp.register_message_handler(
        contact_details, lambda message: kc.GET_CONTACT_DETAILS in message.text)

    dp.register_callback_query_handler(
       send_to_admin, lambda x: x.data and x.data.startswith('Via '))

    dp.register_callback_query_handler(
        click,lambda x: x.data and x.data.startswith('accept '))

    dp.register_message_handler(myorder,lambda message: kc.MY_ORDER == message.text)

    dp.register_message_handler(
        cars2, lambda message:  message.text in car_list)

    dp.register_message_handler(
        back,lambda message: kc.BACK_BUTTON == message.text)
    
    dp.register_callback_query_handler(choice, lambda x: x.data and x.data.startswith('Buy '))


    dp.register_callback_query_handler(cancel_order,lambda x: x.data and x.data.startswith('cancel '))
