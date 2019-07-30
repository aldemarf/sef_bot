import logging
import paho.mqtt.subscribe as subscribe
from quiteria.resources.var import *

logging.getLogger().setLevel(logging.INFO)


def last_messages(topics=('th0/temperature')):

    message = subscribe.simple(topics, hostname=BROKER_URL,
                               retained=True, msg_count=1)
    return message.payload
