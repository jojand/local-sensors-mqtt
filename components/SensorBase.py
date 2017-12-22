import logging
from Ds18b20Mqtt import Ds18b20Mqtt


class SensorBase:

    def init(self):
        raise NotImplementedError()

    def read_values(self):
        raise NotImplementedError()

    def publish(self):
        raise NotImplementedError()

    @staticmethod
    def get_sensor(sensor_configuration):
        constructors = {
            'ds18b20': lambda config: Ds18b20Mqtt(**config)
        }
        try:
            platform = sensor_configuration['platform']
        except :
            logging.error('Excepted element "platform" was not found for a sensor in configuration file.')
            return None

        constructor = constructors[platform]

        if constructor is None:
            logging.error('Platform type "{}" is not supported. Supported platforms are: {}'.format(
                platform, list(constructor.keys())))
            return None

        return constructor(sensor_configuration)
