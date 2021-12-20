
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import keyboards_constants as kc


b1 = KeyboardButton(kc.LIST_OF_CARS)
b2 = KeyboardButton(kc.GET_CONTACT_DETAILS)
b3 = KeyboardButton("❌ Cancel order")
b4 = KeyboardButton("📃 Get Available Options")
b5 = KeyboardButton("📝 Your Order Details")
b6 = KeyboardButton("📲 Share my phone number", request_contact=True)

# order_inline =
# order_inline_markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="💰 BUY f''",callback_data='buy'))

bank = InlineKeyboardButton(text = "Bank",callback_data='bank')
bank_m = InlineKeyboardMarkup(row_width=1).add(bank)
#call = InlineKeyboardButton(text="📞 Call",callback_data=+998123456789)
map = InlineKeyboardButton(
    text="🗺 Location", url="https://maps.app.goo.gl/tmLmp1MFR4V891wb7")
call_map = InlineKeyboardMarkup(row_width=1).add(map)



choices = InlineKeyboardMarkup(row_width=2)

register = KeyboardButton(kc.REGISTER)
cancel_button = KeyboardButton(kc.CANCEL_REG)
back_button = KeyboardButton(kc.BACK_BUTTON)
my_order = KeyboardButton(kc.MY_ORDER)


menu = ReplyKeyboardMarkup(resize_keyboard=True)
phone_number = ReplyKeyboardMarkup(resize_keyboard=True)
registration = ReplyKeyboardMarkup(resize_keyboard=True)

phone_number2 = ReplyKeyboardMarkup(resize_keyboard=True)
registration.add(register, cancel_button)

menu.add(b1)
menu.row(b2,my_order)


phone_number.add(b6).add(back_button)
phone_number2.add(b6)

car_inline_button = InlineKeyboardMarkup(row_width=1)

buy_button = InlineKeyboardButton(text="💰 Buy ")

car_inline_button.add(buy_button)
