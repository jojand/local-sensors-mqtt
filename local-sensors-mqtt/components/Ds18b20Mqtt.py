import logging
from SensorBase import SensorBase
from w1thermsensor import W1ThermSensor


class Ds18b20Mqtt(SensorBase):

    def __init__(self, **kwargs):
        self._name = kwargs['name']
        self._mqtt = kwargs['mqtt']
        self._temperature_topic = kwargs['temperature_topic']
        self._update_interval = kwargs['update_interval']
        self._temperature = None

    def get_update_interval(self):
        return self._update_interval

    def init(self):
        pass

    def read_values(self):
        logging.info('Performing measurement ...')
        self.read_temperature()
        pass

    def publish(self):
        formatted_value = '{0:0.2f}'.format(self._temperature)
        self._mqtt.publish(topic=self._temperature_topic, message=formatted_value)
        pass

    def read_temperature(self):
        sensor_count = len(W1ThermSensor.get_available_sensors())
        if sensor_count == 1:
            sensor = W1ThermSensor.get_available_sensors()[0]
            sensor_id, temperature = (sensor.id, sensor.get_temperature())
            logging.info('Read temperature: {} from sensor id: {}.'.format(temperature, sensor_id))
            self._temperature = temperature
        else:
            logging.error('There are "{}" sensors connected to the GPIO4. Expected: 1.'.format(sensor_count))
            self._temperature = None
