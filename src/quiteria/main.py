# coding=utf-8
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
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name)
                  + " ["
                  + str(m.chat.id)
                  + "]: "
                  + m.text)


# ## BOT INIT & CONFIG ###
bot = telebot.TeleBot(BOT_TOKEN)
bot.set_update_listener(listener)

# ## COMMANDS ###
command_list = {
    'start': 'Iniciar uma conversa com Quitéria',
    'bye': 'Despedir-se de Quitéria',
    'services': 'Listar os serviços disponíveis',
    'help': 'Mostrar esta descrição'}


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    user_tg = message.from_user
    dao = UserDAO()
    result = dao.get_user(user_tg.id)

    if len(result) > 0:
        user = result[0]
        bot.send_message(chat_id, "Olá, {}! \n".format(user.name)
                         + "Deseja logar no sistema?",
                         reply_markup=loginSelection)
    else:
        name = user_tg.first_name
        bot.send_message(chat_id, "Olá, {}! \n".format(name)
                         + "Deseja cadastrar-se no sistema?",
                         reply_markup=registerSelection)


@bot.message_handler(commands=['bye'])
def command_bye(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Sessão encerrada.")
    bot.send_message(chat_id, "Até logo!")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Os seguintes comandos estão disponíveis: \n"

    for key, value in command_list.items():
        help_text += "/" + key + ": " + value + "\n"
    bot.send_message(cid, help_text)


@bot.message_handler(commands=['services'])
def quiteria_menu(message):
    chat_id = message.chat.id
    services_text = "Serviços disponíveis: \n"
    bot.send_message(chat_id, services_text,
                     reply_markup=servicesSelection)


# Default answer for unknown commands
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    bot.reply_to(message, "Não entendi."
                          " Talvez o comando /help possa lhe ajudar.")


# ## CALLBACK HANDLERS ###
@bot.callback_query_handler(func=lambda call: call.data == U_REGISTER_YES)
def cb_register_yes(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.edit_message_reply_markup(chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=hideInlineBoard)
    bot.send_message(chat_id, 'R: Sim')
    bot.send_message(chat_id, 'Deseja aproveitar os dados do telegram?',
                     reply_markup=reuseKeyboard)


@bot.callback_query_handler(func=lambda call: call.data == R_REUSE_YES)
def cb_reuse_yes(call):
    global session
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    tgUser = call.from_user

    bot.edit_message_reply_markup(chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=hideInlineBoard)
    bot.send_message(chat_id, 'R: Sim')
    bot.send_message(chat_id, 'Telegram ID : {}\nNome : {}'
                     .format(tgUser.id, tgUser.first_name))
    session.user = User(telegram_id=tgUser.id,
                        name=tgUser.first_name)
    bot.answer_callback_query(call.id, 'Dados importados com sucesso.')
    bot.send_message(chat_id, 'Agora vamos cadastrar sua senha.')
    msg = bot.send_message(tgUser.id,'Por favor, digite sua senha:',
                           reply_markup=ForceReply(selective=True))
    bot.register_next_step_handler(msg, register_password)


def register_password(message):
    chat_id = message.chat.id
    message_id = message.message_id
    tgUser = message.from_user
    password = message.text

    if len(password) < 4:
        msg = bot.reply_to(message, 'A senha deve ter pelo menos 5 caracteres')
        bot.register_next_step_handler(msg, register_password)
        return
    userSession = Session.SESSIONS[tgUser.id]
    userSession.user
    pass


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
