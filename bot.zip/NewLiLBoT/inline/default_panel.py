from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


main = InlineKeyboardMarkup()
change_panel = InlineKeyboardButton(text='🔄 изменить панель',callback_data='change_menu2')
doxbin = InlineKeyboardButton(text='😈 Doxbin',callback_data='doxbin ')
ddos = InlineKeyboardButton(text='🔥 Ddos',callback_data='ddos')
number = InlineKeyboardButton(text='🎲 Number ',callback_data='number')
database = InlineKeyboardButton(text='📁 Database',callback_data='database')
tg_id  = InlineKeyboardButton(text='🆔 Tg id ',callback_data='tg_id')
vk_id = InlineKeyboardButton(text='🆔  Vk id',callback_data='vk_id')
main.row(change_panel)
main.row(doxbin,ddos)
main.row(number,database)
main.row(tg_id,vk_id)


