from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import keyboards_constants as kc

reject = InlineKeyboardButton(text=kc.REJECT, callback_data='reject')

remove = InlineKeyboardButton(text=kc.REMOVE, callback_data='delete')


add = KeyboardButton(kc.ADD)
list_cars = KeyboardButton(kc.LIST_CARS)
cancel_button = KeyboardButton(kc.CANCEL_BUTTON)
back = KeyboardButton(kc.BACK)
orders = KeyboardButton(kc.GET_LIST)
add_contact = KeyboardButton(kc.ADD_CONTACT)

admin_a_r = InlineKeyboardMarkup(row_width=2).add(reject)
remove_inl_button = InlineKeyboardMarkup(row_width=1).add(remove)


admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu2 = ReplyKeyboardMarkup(resize_keyboard=True)


admin_menu.add(add).add(list_cars).add(add_contact).add(orders)

admin_menu2.add(add).add(cancel_button).add(back)
