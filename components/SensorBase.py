import logging


class SensorBase:

    def __init__(self, platform):
        self._platform = platform

    def init(self):
        raise NotImplementedError()

    def read_values(self):
        raise NotImplementedError()

    def publish(self):
        raise NotImplementedError()

    @staticmethod
    def get_sensor(mqtt, sensor_config):
        from Ds18b20Mqtt import Ds18b20Mqtt
        from HTU21 import HTU21
        from Bmp180 import Bmp180
        constructors = {
            'ds18b20': lambda mqtt, config: Ds18b20Mqtt(mqtt=mqtt, **config),
            'HTU21': lambda mqtt, config: HTU21(mqtt=mqtt, **config),
            'Bmp180': lambda mqtt, config: Bmp180(mqtt=mqtt, **config)
        }
        try:
            platform = sensor_config['platform']
        except:
            logging.error('Excepted element "platform" was not found for a sensor in configuration file.')
            return None

        constructor = constructors[platform]

        if constructor is None:
            logging.error('Platform type "{}" is not supported. Supported platforms are: {}'.format(
                platform, list(constructor.keys())))
            return None

        return constructor(mqtt, sensor_config)
