from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from quiteria.resources.strings import *


# ## INLINE KEYBOARDS ###
servicesSelection = InlineKeyboardMarkup(row_width=1)
servicesSelection.add(InlineKeyboardButton('Ajuste de temperatura',
                                           callback_data=SERV_TEMP),
                      InlineKeyboardButton('Agendamento de sala',
                                           callback_data=SERV_ROOM),
                      InlineKeyboardButton('Agendamento de manutenção',
                                           callback_data=SERV_MNT),
                      InlineKeyboardButton('Leitura de sensores',
                                           callback_data=SERV_SENS))

loginSelection = InlineKeyboardMarkup(row_width=2)
loginSelection.add(InlineKeyboardButton("Sim",
                                        callback_data=U_LOGIN_YES),
                   InlineKeyboardButton("Não",
                                        callback_data=U_LOGIN_NO))

registerSelection = InlineKeyboardMarkup(row_width=2)
registerSelection.add(InlineKeyboardButton("Sim",
                                           callback_data=U_REGISTER_YES),
                      InlineKeyboardButton("Não",
                                           callback_data=U_REGISTER_NO))

yesNoSelection = InlineKeyboardMarkup(row_width=2)
yesNoSelection.add(InlineKeyboardButton('Sim', callback_data=ANS_YES),
                   InlineKeyboardButton('Não', callback_data=ANS_NO, ))


reuseKeyboard = InlineKeyboardMarkup(row_width=2)
reuseKeyboard.add(InlineKeyboardButton('Sim', callback_data=R_REUSE_YES),
                  InlineKeyboardButton('Não', callback_data=R_REUSE_NO))

hideInlineBoard = InlineKeyboardMarkup()


# ## REPLY KEYBOARDS ###
hideBoard = ReplyKeyboardRemove()

