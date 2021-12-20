from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from config import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_contact_db, sqlite_db
from data_base.orders import admin_oreders_read
from handlers import client
from keyboards import admin_menu, admin_menu2
import keyboards_constants as kc
ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


class FSMAdmin_office(StatesGroup):
    location = State()
    adress = State()
    phone_number = State()
    email = State()

# @dp.message_handler(commands=['moderator'],is_chat_admin=True)


async def make_changes_command(message: types.Message):
    # if not message.from_user.id in ID:
    #     ID.append(message.from_user.id)
    global ID
    ID  = message.from_user.id
    await bot.send_message(message.from_user.id, "👨‍💻 Hello Admin!", reply_markup=admin_menu)
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEDcSJhsafdtfY_LsVl01PGj8sUbAGGtwACAQEAAladvQoivp8OuMLmNCME")
    await message.delete()


# FSM STARTING POINT of ADDING NEW CAR TO DATABASE
# @dp.message_handler(commands='Download',state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.answer("🏗 You started creating model")
        await message.reply("Upload car's photo", reply_markup=admin_menu2)


# @dp.message_handler(state="*",commands='Cancel')
# @dp.message_handler(Text(equals='Cancel',ignore_case=True),state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('✅ Process is canceled successfully')


# @dp.message_handler(content_types=['photo'],state = FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Enter name of car")


# @dp.message_handler(state = FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Fill description of the car")


# @dp.message_handler(state = FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Price of the car")


# @dp.message_handler(state = FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text

        await bot.send_message(message.from_user.id, "✅ Successfully completed")
        await sqlite_db.sql_add_command(state)
        await state.finish()
# FSM ENDING POINT of ADDING NEW CAR TO DATABASE


# ADDING CONTACT DETAILS

async def cm_start_contact(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin_office.location.set()
        await bot.send_message(message.from_user.id, "🗺 Send 🏢 office location link")


async def load_location(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data2:
            data2['location'] = message.text
        await FSMAdmin_office.next()
        await message.reply("Fill the address of office 👇")


async def load_address(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data2:
            data2['address'] = message.text
        await FSMAdmin_office.next()
        await message.reply("📞 Fill office phone number 👇")


async def load_phone_number(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data2:
            data2['phone_number'] = message.text
        await FSMAdmin_office.next()
        await message.reply("📧 Fill office e-mail👇")


async def load_email(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data2:
            data2['email'] = message.text
        await bot.send_message(message.from_user.id, "✅ Successfully completed")
        await sqlite_contact_db.sql_add_command_contact(state)
        await state.finish()
# FSM ENDING POINT of ADDING CONTACT DETAILS TO DATABASE



async def accept_c(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_sticker(client.iduser, sticker='CAACAgIAAxkBAAEDcXphsex6e7VMenBvD0uX9p_raQtcuQAC_gADVp29CtoEYTAu-df_IwQ')
    await bot.send_message(client.iduser, "✅ Order accepted. Make payment to this #1234567890 bank account")


async def reject_c(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(client.iduser, "❌ Order rejected")



async def car_menu_admin_command(message: types.Message):
    await sqlite_db.sql_read_admin(message)



async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'🚗 Model:  {ret[1]}\n📝 Description:  {ret[2]}\n💸 Price:   {ret[-1]} UZS',
             reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=f'🗑 Remove {ret[1]}',
              callback_data=f'del {ret[1]}')))


# @dp.callback_query_handler(lambda x: x.data and x.data.startwith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ","")} 🗑 Deleted.', show_alert=True)




async def back_admin(message: types.Message):
    await message.answer("Main menu",reply_markup=admin_menu)
    await message.delete()


async def orders_list(message: types.Message):
    await admin_oreders_read()

# REGISTERING MESSAGE AND CALLBACK HANDLERS TO EXPORT TO TELE_BOT.PY
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        cm_start, lambda message: kc.ADD in message.text, state=None)

    dp.register_message_handler(cancel_handler, Text(
        equals=kc.CANCEL_BUTTON, ignore_case=True), state="*")

    dp.register_message_handler(make_changes_command, commands=[
                                'moderator'], is_chat_admin=True)

    dp.register_message_handler(load_photo, content_types=[
                                'photo'], state=FSMAdmin.photo)

    dp.register_message_handler(load_name, state=FSMAdmin.name)

    dp.register_message_handler(load_description, state=FSMAdmin.description)

    dp.register_message_handler(load_price, state=FSMAdmin.price)

    #dp.register_message_handler(cancel_handler, state="*", commands='Cancel')

    dp.register_callback_query_handler(accept_c, text='bank')

    dp.register_callback_query_handler(reject_c, text='reject')

    dp.register_message_handler(
        delete_item, lambda message: kc.LIST_CARS in message.text)

    dp.register_callback_query_handler(
        del_callback_run, lambda x: x.data and x.data.startswith('del '))

    dp.register_message_handler(back_admin,lambda message: kc.BACK == message.text)    


# REGISTERING MESSAGE AND CALLBACK HANDLERS TO EXPORT TO TELE_BOT.PY
def register_handlers_admin_contacts(dp: Dispatcher):
    
    dp.register_message_handler(
        cm_start_contact, lambda message: kc.ADD_CONTACT in message.text, state=None)

    dp.register_message_handler(load_location, state=FSMAdmin_office.location)

    dp.register_message_handler(load_address, state=FSMAdmin_office.adress)

    dp.register_message_handler(load_phone_number, state=FSMAdmin_office.phone_number)

    dp.register_message_handler(load_email, state=FSMAdmin_office.email)

    dp.register_message_handler(orders_list,lambda message: kc.GET_LIST == message.text)
