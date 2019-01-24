from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from components.Mqtt import Mqtt

import logging
import argparse
import thread
import time
import signal

update_interval = 10
sensors = []
mqtt = None
interrupted = False


def init_logging(logging_path):
    logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s [%(levelname)s]: %(message)s',
                        filename=logging_path, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())


def get_config_item(config_data, item):
    try:
        return config_data[item]
    except Exception as e:
        logging.error('"{}" configuration item not found in configuration file.'.format(item))


def init_sensors(config_sensors, mqtt):
    from components.SensorBase import SensorBase
    if len(config_sensors) < 1:
        logging.error('Number of sensors must be >= 1')
        raise RuntimeError
    for sensor_config in config_sensors:
        logging.info('Found sensor in configuration: {}'.format(sensor_config))
        sensor_object = SensorBase.get_sensor(mqtt, sensor_config)
        sensor_object.init()
        sensors.append(sensor_object)


def load_config(config_path):
    global update_interval
    logging.info('Using config file: {}'.format(config_path))
    config_data = load(open(config_path).read())
    config_general = get_config_item(config_data, 'general')
    config_mqtt = get_config_item(config_data, 'mqtt')
    config_sensors = get_config_item(config_data, 'sensors')
    update_interval = config_general['update_interval']
    mqtt = Mqtt(**config_mqtt)
    # print config_sensors
    init_sensors(config_sensors, mqtt)


def measure_loop(thread_name, delay):
    while True:
        logging.info('In thread {}'.format(thread_name))
        read_and_publish()
        time.sleep(delay)


def measure_loop_sensor(thread_name, sensor):
    while True:
        logging.info('In thread {}'.format(sensor))
        sensor.read_values()
        sensor.publish()
        time.sleep(sensor.get_update_interval())


def read_and_publish():
    for sensor in sensors:
        sensor.read_values()
        sensor.publish()


def interrupt_handler(signal, frame):
    global interrupted
    interrupted = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file', required=True)
    parser.add_argument('-l', '--logpath', help='Log file path', required=True)
    args = parser.parse_args()

    init_logging(args.logpath)
    logging.info('Starting local-sensors-mqtt ...')
    logging.info('Using log file: {}'.format(args.logpath))
    load_config(args.config)

    signal.signal(signal.SIGINT, interrupt_handler)

    while True:
        # logging.info('Main loop tick')
        measure_loop('main', 60)
        if interrupted:
            break

    logging.info('Exit')


if __name__ == "__main__":
    main()
