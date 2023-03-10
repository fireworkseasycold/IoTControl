import paho.mqtt.client as mqtt
from functools import lru_cache

from .models import Messages


class Mqtt():
    TOPICS = [
        'DHT22/temperature',
        'DHT22/humidity',
        'webApp/actuator'
    ]

    def __init__(self):
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.loop_started = False
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        print('Connected!')
        self.subscribe(self.TOPICS)

    @staticmethod
    def on_message(client, userdata, msg):
        print(f'msg_topic:{msg.topic} message:{str(msg.payload)}')

        message = Messages(
            topic=msg.topic,
            device=msg.topic,
            message=msg.payload.decode('utf-8'),
            type=Messages.RECEIVED
        )

        message.save()

    def get_client(self):
        return self.client

    def publish_message(self, topic, message):
        if not self.connected:
            return

        self.client.publish(topic, message)

        new_message = Messages(
            topic=topic,
            device="webApp",
            message=message,
            type=Messages.SENT
        )

        new_message.save()

    def connect(self, connection_address):
        if self.connected:
            return

        self.client.connect(connection_address)
        self.connected = True

    def subscribe(self, topics):
        if not self.connected:
            return

        print(topics)
        for topic in topics:
            self.client.subscribe(topic)
            print(f'subscribed in {topic}')

    def start_loop(self):
        if self.loop_started:
            return

        if not self.connected:
            return

        self.client.loop_start()
        self.loop_started = True
        print('started_loop!')


@lru_cache(maxsize=None)
def get_mqtt():
    return Mqtt()
