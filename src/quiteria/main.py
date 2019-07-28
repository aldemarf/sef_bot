# coding=utf-8
import logging

from collections import OrderedDict

import telebot
from telebot.types import ForceReply

from quiteria.domain.session import *
from quiteria.domain.user import User
from quiteria.keyboards.keyboards import *
from quiteria.resources.var import *
from quiteria.resources.strings import *
from quiteria.persistence.sqlite import UserDAO, SQLiteDB


# ##  DATABASE INIT ###
SQLiteDB.create_tables()


# ## SESSION ###
session = None


# ## LISTENER | LOG ###
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for message in messages:
        if message.content_type == 'text':
            # print the sent message to the console
            logging.info(
                '{} [{}]: {}'
                    .format(message.chat.first_name,
                            message.chat.id,
                            message.text))


# ## BOT INIT & CONFIG ###
bot = telebot.TeleBot(BOT_TOKEN)
bot.set_update_listener(listener)

# ## COMMANDS ###
command_list = OrderedDict({
    'unlogged':'**Usuários não logados**:',
    'start': 'Iniciar uma conversa com Quitéria',
    'help': 'Mostrar esta descrição',
    'bye': 'Despedir-se de Quitéria',
    'logged':'**Usuários logados**:',
    'services': 'Listar os serviços disponíveis'
})


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    tgUser = message.from_user
    dao = UserDAO()
    result = dao.get_user(tgUser.id)

    Session.setSession(tgUser.id)

    if len(result) > 0:
        user = result[0]
        bot.send_message(chat_id, "Olá, {}! \n".format(user.name)
                         + "Deseja logar no sistema?",
                         reply_markup=loginSelection)
    else:
        name = tgUser.first_name
        bot.send_message(chat_id, "Olá, {}! \n".format(name)
                         + "Deseja cadastrar-se no sistema?",
                         reply_markup=registerSelection)


@bot.message_handler(commands=['bye'])
def command_bye(message):
    chatID = message.chat.id
    tgUserID = message.from_user.id

    try:
        Session.endSession(tgUserID)
        bot.send_message(chatID, "Sessão encerrada.")
        bot.send_message(chatID, "Até logo!")
    except Exception:
        logging.error('Sessão não encontrada.', exc_info=True)


@bot.message_handler(commands=['help'])
def command_help(message):
    chatID = message.chat.id
    helpText = "Os seguintes comandos estão disponíveis: \n"

    for key, value in command_list.items():
        if key.endswith('logged'):
            helpText += '\n\n{}\n'.format(value)
            continue
        helpText += '/{} : {}\n'.format(key, value)
    bot.send_message(chatID, helpText, parse_mode='MARKDOWN')


@bot.message_handler(commands=['services'])
def quiteria_menu(message):
    tgUserID = message.from_user.id
    session = Session.sessions[tgUserID]

    if not session.logged:
        bot.send_message(tgUserID,
                         'Serviços disponíveis apenas para'
                         ' usuários logados no sistema.')
        return

    chatID = message.chat.id
    services_text = "Serviços disponíveis: \n"
    bot.send_message(chatID, services_text,
                     reply_markup=servicesSelection)


# Default answer for unknown commands
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    bot.reply_to(message, "Não entendi."
                          " Talvez o comando /help possa lhe ajudar.")


# ## CALLBACK HANDLERS ###
@bot.callback_query_handler(func=lambda call: call.data == U_REGISTER_YES)
def cb_register_yes(call):
    chatID = call.message.chat.id
    messageID = call.message.message_id
    bot.edit_message_reply_markup(chat_id=chatID,
                                  message_id=messageID,
                                  reply_markup=hideInlineBoard)
    bot.send_message(chatID, 'R: Sim')
    bot.send_message(chatID, 'Deseja aproveitar os dados do telegram?',
                     reply_markup=reuseKeyboard)


@bot.callback_query_handler(func=lambda call: call.data == R_REUSE_YES)
def cb_reuse_yes(call):
    chatID = call.message.chat.id
    messageID = call.message.message_id
    tgUser = call.from_user
    userSession = Session.sessions[tgUser.id]

    bot.edit_message_reply_markup(chat_id=chatID,
                                  message_id=messageID,
                                  reply_markup=hideInlineBoard)

    bot.send_message(chatID, 'R: Sim')
    bot.send_message(chatID, 'Telegram ID : {}\nNome : {}'
                     .format(tgUser.id, tgUser.first_name))
    userSession.user = User(telegram_id=tgUser.id,
                        name=tgUser.first_name)
    bot.answer_callback_query(call.id, 'Dados importados com sucesso.')

    bot.send_message(chatID, 'Agora vamos cadastrar sua senha.')
    msg = bot.send_message(tgUser.id,'Por favor, digite sua senha:',
                           reply_markup=ForceReply(selective=True))
    bot.register_next_step_handler(msg, register_password)


def register_password(message):
    chatID = message.chat.id
    messageID = message.message_id
    tgUserID = message.from_user.id
    password = message.text
    userSession = Session.sessions[tgUserID]

    bot.delete_message(chatID,messageID)
    bot.send_message(chatID, '****')

    if len(password) < 4:
        msg = bot.send_message(chatID,
                               'A senha deve ter no mínimo 4 caracteres')
        bot.register_next_step_handler(msg, register_password)
        return

    userSession.user.password = password

    msg = bot.send_message(tgUserID, 'Por favor, repita senha:',
                           reply_markup=ForceReply(selective=True))
    bot.register_next_step_handler(msg, confirm_password)

def confirm_password(message):
    chatID = message.chat.id
    messageID = message.message_id
    tgUserID = message.from_user.id
    confirmPwd = message.text
    userSession = Session.sessions[tgUserID]

    bot.delete_message(chatID, messageID)
    bot.send_message(chatID, '****')

    if len(confirmPwd) < 4 or confirmPwd != userSession.user.password:
        msg = bot.send_message(chatID, 'A senha deve ter no mínimo 4'
                                        ' caracteres e ser igual a anterior',
                               reply_markup=ForceReply(selective=True))
        bot.register_next_step_handler(msg, confirm_password)
        return

    bot.send_message(tgUserID, 'Senha configurada com sucesso.')

    dao = UserDAO()
    dao.insert_user(userSession.user)


@bot.callback_query_handler(func=lambda call: call.data == ANS_YES)
def cb_login_yes(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.send_message(chat_id, 'R: Sim')
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                  reply_markup=hideInlineBoard)


@bot.callback_query_handler(func=lambda call: call.data == ANS_NO)
def cb_login_no(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.answer_callback_query(call.id, "Answer is No", show_alert=True)
    bot.send_message(chat_id, 'R: Não')
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                  reply_markup=hideInlineBoard)


# ## START BOT LISTENING ###
bot.polling()
