# coding=utf-8
import logging

# ## LOGGIN ###
logging.getLogger().setLevel(logging.INFO)  # Set log level
logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

# ## QUITERIA PARAMETERS ###
MIN_PWD_LENGHT = 4
MAX_LOGIN_ATTEMPTS = 3