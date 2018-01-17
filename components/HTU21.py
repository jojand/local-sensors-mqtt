import logging
from SensorBase import SensorBase
import HTU21DF


class HTU21(SensorBase):

    def __init__(self, **kwargs):
        self._name = kwargs['name']
        self._mqtt = kwargs['mqtt']
        self._temperature_topic = kwargs['temperature_topic']
        self._humidity_topic = kwargs['humidity_topic']
        self._update_interval = kwargs['update_interval']
        self._temperature = None
        self._humidity = None

    def get_update_interval(self):
        return self._update_interval

    def init(self):
        HTU21DF.htu_reset()

    def read_values(self):
        logging.info('Performing measurement ...')
        self._temperature = HTU21DF.read_temperature()
        self._humidity = HTU21DF.read_humidity()
        logging.info('Got measurement: temperature: {}, humidity: {}'.format(self._temperature, self._temperature))

    def publish(self):
        formatted_temperature = '{0:0.2f}'.format(self._temperature)
        self._mqtt.publish(topic=self._temperature_topic, message=formatted_temperature)
        formatted_humidity = '{0:0.2f}'.format(self._humidity)
        self._mqtt.publish(topic=self._humidity_topic, message=formatted_humidity)


