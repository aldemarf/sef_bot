import logging
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import sys
from var import *

logging.getLogger().setLevel(logging.INFO)

subscribeTopic = DHT_TOPIC

def on_connect(client, userdata, flags, rc):
    logging.info('Conectando ao broker... Status : {}'.format(rc))

    client.subscribe(subscribeTopic)


def on_message(client, userdata, msg):
    MensagemRecebida = str(msg.payload)

    logging.info('Tópico: {}    Mensagem: {}'
                 .format(msg.topic, MensagemRecebida))

def start_subscribe():
    try:
        logging.info('Inicializando MQTT...')

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(BROKER_URL, BROKER_PORT, KEEP_ALIVE_BROKER)
        client.loop_forever()

    except KeyboardInterrupt:
        logging.error('Saida forçada. Encerrando aplicação...')
        sys.exit(0)


def last_Message(topics=(TEMPERATURE_TOPIC, HUMIDITY_TOPIC)):
    message = subscribe.simple(topics, hostname=BROKER_URL,
                                retained=False,
                                msg_count=1)
    return message

if __name__ == '__main__':
    last_Message()