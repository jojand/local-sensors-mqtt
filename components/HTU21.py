import logging
from SensorBase import SensorBase
from smbus import SMBus
import time


I2C_ADDR = 0x40
CMD_TRIG_TEMP_HM = 0xE3
CMD_TRIG_HUMID_HM = 0xE5
CMD_TRIG_TEMP_NHM = 0xF3
CMD_TRIG_HUMID_NHM = 0xF5
CMD_WRITE_USER_REG = 0xE6
CMD_READ_USER_REG = 0xE7
CMD_RESET = 0xFE


class HTU21(SensorBase):

    def __init__(self, **kwargs):
        self._name = kwargs['name']
        self._mqtt = kwargs['mqtt']
        self._temperature_topic = kwargs['temperature_topic']
        self._humidity_topic = kwargs['humidity_topic']
        self._update_interval = kwargs['update_interval']
        self._bus_number = kwargs['bus_number']
        self._temperature = None
        self._humidity = None
        self._sm_bus = SMBus(self._bus_number)

    def get_update_interval(self):
        return self._update_interval

    def init(self):
        self._reset()

    def read_values(self):
        logging.info('Performing measurement ...')
        self._temperature = self._read_temperature()
        self._humidity = self._read_humidity()
        logging.info('Got measurement: temperature: {}, humidity: {}'.format(self._temperature, self._temperature))

    def publish(self):
        formatted_temperature = '{0:0.2f}'.format(self._temperature)
        self._mqtt.publish(topic=self._temperature_topic, message=formatted_temperature)
        formatted_humidity = '{0:0.2f}'.format(self._humidity)
        self._mqtt.publish(topic=self._humidity_topic, message=formatted_humidity)

    def _reset(self):
        # self._sm_bus = SMBus(self._bus_number)
        time.sleep(0.5)
        self._sm_bus.write_byte(I2C_ADDR, CMD_RESET)

    def _read_temperature(self):
        self._reset()
        time.sleep(0.5)
        msb, lsb, crc = self._sm_bus.read_i2c_block_data(I2C_ADDR, CMD_TRIG_TEMP_HM, 3)
        return -46.85 + 175.72 * (msb * 256 + lsb) / 65536

    def _read_humidity(self):
        self._reset()
        time.sleep(0.5)
        msb, lsb, crc = self._sm_bus.read_i2c_block_data(I2C_ADDR, CMD_TRIG_HUMID_HM, 3)
        return -6 + 125 * (msb * 256 + lsb) / 65536.0

