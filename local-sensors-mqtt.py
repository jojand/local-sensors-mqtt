from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from components.Mqtt import Mqtt
import logging

CONFIG_PATH = 'resources/configuration.yml'
LOGGING_PATH = 'local-sensors-mqtt.log'

sensors = []
mqtt = None

def init_logging():
    logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s [%(levelname)s]: %(message)s',
                        filename=LOGGING_PATH, level=logging.INFO)

def get_config_item(config_data, item):
    try:
        return config_data[item]
    except Exception as e:
        logging.error('"{}" configuration item not found in configuration file.'.format(item))

def init_sensors(config_sensors):
    if len(sensors) < 1:
        logging.error('Number of sensors must be >= 1')
        raise RuntimeError
    for sensor in config_sensors:



def load_config():
    config_data = load(open(CONFIG_PATH).read())

    config_mqtt = get_config_item('mqtt')
    config_sensors = get_config_item('sensors')

    mqtt = Mqtt(**config_mqtt)



def main():
    init_logging()
    logging.info('Starting local-sensors-mqtt ...')
    config_data = load(open(CONFIG_PATH).read())
    config_mqtt = config_data[]

if __name__ == "__main__":
    main()
