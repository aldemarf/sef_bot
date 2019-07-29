# coding=utf-8
from collections import OrderedDict

import telebot
from telebot.types import ForceReply

from quiteria.domain.session import *
from quiteria.domain.user import User
from quiteria.keyboards.keyboards import *
from quiteria.resources.settings import *
from quiteria.resources.var import *
from quiteria.resources.strings import *
from quiteria.persistence.sqlite import UserDAO, SQLiteDB

# ##  DATABASE INIT ###
SQLiteDB.create_tables()


# ## LISTENER | LOG ###
def listener(messages):
    for message in messages:
        if message.content_type == 'text':
            # print the sent message to the console
            logging.info(
                '{} [{}]: {}'.format(message.chat.first_name,
                                     message.chat.id,
                                     message.text))


# ## BOT INIT & CONFIG ###
bot = telebot.TeleBot(BOT_TOKEN)
bot.set_update_listener(listener)


# ## COMMANDS ###
command_list = OrderedDict({
    'unlogged': '**Usuários não logados**:',
    'start': 'Iniciar uma conversa com Quitéria',
    'login': 'Realizar login no sistema',
    'help': 'Mostrar esta descrição',
    'bye': 'Despedir-se de Quitéria (sair do sistema)',
    'logged': '**Usuários logados**:',
    'services': 'Listar os serviços disponíveis'
})


@bot.message_handler(commands=['start'])
def command_start(message):
    chatID = message.chat.id
    tgUser = message.from_user
    dao = UserDAO()
    result = dao.get_user(tgUser.id)
    logging.info('{} resultado(s) encontrado(s)'.format(len(result)))

    Session.setSession(tgUser.id)

    helpText = "Os seguintes comandos estão disponíveis: \n"

    for key, value in command_list.items():
        if key.endswith('logged'):
            helpText += '\n\n{}\n'.format(value)
            continue
        helpText += '/{} : {}\n'.format(key, value)
    bot.send_message(chatID, helpText, parse_mode='MARKDOWN')

    if len(result) > 0:
        user = result
        bot.send_message(chatID, "Olá, {}! \n".format(user.name)
                         + "Deseja logar no sistema?",
                         reply_markup=loginSelection)
    else:
        name = tgUser.first_name
        bot.send_message(chatID, "Olá, {}! \n".format(name)
                         + "Deseja cadastrar-se no sistema?",
                         reply_markup=registerSelection)


@bot.message_handler(commands=['login'])
def command_login(message):
    tgUserID = message.from_user.id
    dao = UserDAO()
    user = dao.get_user(tgUserID)

    try:
        session = Session.sessions[tgUserID]
    except KeyError:
        session = Session.setSession(tgUserID)

    if user:
        session.user = user
        msg = bot.send_message(tgUserID, 'Por favor, digite sua senha:',
                               reply_markup=ForceReply(selective=True))
        bot.register_next_step_handler(msg, do_login)
    else:
        bot.send_message(tgUserID, "Deseja cadastrar-se no sistema?",
                         reply_markup=registerSelection)


@bot.message_handler(commands=['bye'])
def command_bye(message):
    chatID = message.chat.id
    tgUserID = message.from_user.id

    try:
        Session.endSession(tgUserID)
        bot.send_message(chatID, "Sessão encerrada.")
        bot.send_message(chatID, "Até logo!")
    except KeyError:
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
    logging.info('User logged: {}'.format(session.logged))

    if not session.logged:
        bot.send_message(tgUserID,
                         'Serviços disponíveis apenas para usuários logados'
                         ' no sistema. Por favor, realize o login e tente'
                         ' novamente.')
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
    bot.send_message(chatID, 'Deseja utilzar o nome cadastrado no telegram?',
                     reply_markup=reuseKeyboard)


@bot.callback_query_handler(func=lambda call: call.data == R_REUSE_YES)
def cb_reuse_yes(call):
    chatID = call.message.chat.id
    messageID = call.message.message_id
    tgUser = call.from_user
    userSession = Session.sessions[tgUser.id]

    bot.edit_message_reply_markup(chat_id=chatID, message_id=messageID,
                                  reply_markup=hideInlineBoard)

    bot.send_message(chatID, 'R: Sim')
    bot.send_message(chatID, 'Nome : {}'.format(tgUser.first_name))

    userSession.user = User(telegram_id=tgUser.id, name=tgUser.first_name)

    bot.answer_callback_query(call.id, 'Dados importados com sucesso.')

    bot.send_message(chatID, 'Agora vamos cadastrar sua senha.')
    msg = bot.send_message(tgUser.id, 'Por favor, digite sua senha:',
                           reply_markup=ForceReply(selective=True))
    bot.register_next_step_handler(msg, register_password)


@bot.callback_query_handler(func=lambda call: call.data == R_REUSE_NO)
def cb_reuse_no(call):
    chatID = call.message.chat.id
    messageID = call.message.message_id
    tgUser = call.from_user
    userSession = Session.sessions[tgUser.id]

    bot.edit_message_reply_markup(chat_id=chatID, message_id=messageID,
                                  reply_markup=hideInlineBoard)

    bot.send_message(chatID, 'R: Não')
    userSession.user = User(telegram_id=tgUser.id)

    bot.send_message(chatID, 'Vamos começar pelo seu nome.')
    msg = bot.send_message(tgUser.id, 'Por favor, digite seu nome:',
                           reply_markup=ForceReply(selective=True))
    bot.register_next_step_handler(msg, register_name)


def has_number(sentence):
    return any(char.isdigit() for char in sentence)


def register_name(message):
    chatID = message.message.chat.id
    messageID = message.message.message_id
    tgUser = message.from_user
    userSession = Session.sessions[tgUser.id]
    name = message.text

    if name < 2 or has_number(name):
        bot.delete_message(chatID, messageID)
        msg = bot.send_message(chatID, 'Nome inválido. Tente novamente.')
        bot.register_next_step_handler(msg, register_name)
        return

    userSession.user.name = name
    logging.info('Nome cadastrado : {}'.format(name))

    msg = bot.send_message(tgUser.id, 'Por favor, digite uma senha:'
                                      ' (mín. 4 caracteres)',
                           reply_markup=ForceReply(selective=True))
    bot.register_next_step_handler(msg, register_password)


def register_password(message):
    chatID = message.chat.id
    messageID = message.message_id
    tgUserID = message.from_user.id
    password = message.text
    userSession = Session.sessions[tgUserID]

    bot.delete_message(chatID, messageID)
    bot.send_message(chatID, '****')

    if len(password) < MIN_PWD_LENGHT:
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

    if len(confirmPwd) < MIN_PWD_LENGHT \
            or confirmPwd != userSession.user.password:
        msg = bot.send_message(chatID, 'A senha deve ter no mínimo 4'
                                       ' caracteres e ser igual a anterior',
                               reply_markup=ForceReply(selective=True))
        bot.register_next_step_handler(msg, register_password)
        return

    bot.send_message(tgUserID, 'Senha configurada com sucesso.')

    dao = UserDAO()
    userSession.user.id = dao.insert_user(userSession.user)

    bot.send_message(tgUserID, 'Seu cadastro foi concluído.\n'
                               'Deseja realizar o login?',
                     reply_markup=loginSelection)


@bot.callback_query_handler(func=lambda call: call.data == U_LOGIN_YES)
def cb_login_yes(call):
    chatID = call.message.chat.id
    messageID = call.message.message_id
    tgUserID = call.message.from_user.id

    bot.send_message(chatID, 'R: Sim')
    bot.edit_message_reply_markup(chat_id=chatID, message_id=messageID,
                                  reply_markup=hideInlineBoard)

    msg = bot.send_message(tgUserID, 'Ok. Por favor, digite sua senha:',
                           reply_markup=ForceReply(selective=True))

    bot.register_next_step_handler(msg, do_login)


def do_login(message):
    chatID = message.chat.id
    messageID = message.message_id
    tgUserID = message.from_user.id
    password = message.text

    session = Session.sessions[tgUserID]
    session.loginAttempts += 1
    user = session.user

    bot.delete_message(chatID, messageID)
    lastBotMsg = bot.send_message(chatID, '****').message_id

    if password != user.password:
        bot.delete_message(chatID, lastBotMsg)
        leftAttempts = MAX_LOGIN_ATTEMPTS - session.loginAttempts
        msg = bot.send_message(chatID,
                               'Senha inválida. Por favor, tente novamente.\n'
                               '{} tentativas restantes'.format(leftAttempts),
                               reply_markup=ForceReply(selective=True))
        bot.register_next_step_handler(msg, do_login)

    session.logged = True
    session.loginAttempts = 0
    session.startSession(tgUserID)
    bot.send_message(chatID, 'Login realizado com sucesso!')


@bot.callback_query_handler(func=lambda call: call.data == U_LOGIN_NO)
def cb_login_no(call):
    chatID = call.message.chat.id
    messageID = call.message.message_id
    bot.send_message(chatID, 'R: Não')
    bot.edit_message_reply_markup(chat_id=chatID, message_id=messageID,
                                  reply_markup=hideInlineBoard)
    bot.send_message(chatID, 'Ok, mas terei recursos limitados'
                             ' para lhe ajudar.')


# ## START BOT LISTENING ###
bot.polling()
