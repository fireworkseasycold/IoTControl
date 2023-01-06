from django.apps import AppConfig


class WebappConfig(AppConfig):
    name = 'webApp'

    def ready(self):
        from webApp.services import get_mqtt

        mqtt = get_mqtt()

        mqtt.connect('127.0.0.1')
        mqtt.start_loop()
