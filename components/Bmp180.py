import Adafruit_BMP.BMP085 as BMP085
import logging
import time
from SensorBase import SensorBase

NORMALISED_PRESSURE_CONSTANT = 8.3


class Bmp180(SensorBase):

    def __init__(self, **kwargs):
        self._name = kwargs['name']
        self._mqtt = kwargs['mqtt']
        self._temperature_topic = kwargs['temperature_topic']
        self._abs_pressure_topic = kwargs['abs_pressure_topic']
        self._rel_pressure_topic = kwargs['rel_pressure_topic']
        self._update_interval = kwargs['update_interval']
        self._altitude = kwargs['altitude']
        self._bmp085 = None
        self._temperature = -999.0
        self._pressure = -999.0
        self._normalized_pressure = -999.0

    def init(self):
        self._bmp085 = BMP085.BMP085()
        pass

    def read_values(self):
        logging.info('Performing measurements ...')
        self._temperature = self._bmp085.read_temperature()
        self._pressure = self._bmp085.read_pressure() / 100.0
        self._normalized_pressure = self.get_normalized_pressure()
        pass

    def publish(self):
        logging.info('Publishing measurements ...')
        self._publish(self._temperature_topic, self._temperature)
        self._publish(self._rel_pressure_topic,  self._normalized_pressure)
        self._publish(self._abs_pressure_topic, self._pressure)
        pass

    def get_normalized_pressure(self):
        return self._pressure + self._altitude/NORMALISED_PRESSURE_CONSTANT

    def _publish(self, topic, value):
        formatted_value = '{0:0.2f}'.format(value)
        self._mqtt.publish(topic=topic, message=formatted_value)
