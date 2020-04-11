import logging
import math
import pigpio
import time
from SensorBase import SensorBase


class HTU21(SensorBase):
    htu_addr = 0x40
    bus = 1
    cmd_rdtemp = 0xE3
    cmd_rdhumi = 0xE5
    cmd_wtreg = 0xE6
    cmd_rdreg = 0xE7
    cmd_reset = 0xFE

    def __init__(self, **kwargs):
        self._pi = None
        self._name = kwargs['name']
        self._mqtt = kwargs['mqtt']
        self._temperature_topic = kwargs['temperature_topic']
        self._humidity_topic = kwargs['humidity_topic']
        self._update_interval = kwargs['update_interval']
        self._pigpio_host = kwargs['pigpio_host']
        self._pigpio_port = kwargs['pigpio_port']
        self._temperature = None
        self._humidity = None

    def get_update_interval(self):
        return self._update_interval

    def init(self):
        self._pi = pigpio.pi(host=self._pigpio_host, port=self._pigpio_port)
        self.htu_reset()

    def read_values(self):
        logging.info('Performing measurement ...')
        self._temperature = self.read_temperature()
        self._humidity = self.read_humidity()
        logging.info('Got measurement: temperature: {}, humidity: {}'.format(self._temperature, self._temperature))

    def publish(self):
        formatted_temperature = '{0:0.2f}'.format(self._temperature)
        self._mqtt.publish(topic=self._temperature_topic, message=formatted_temperature)
        formatted_humidity = '{0:0.2f}'.format(self._humidity)
        self._mqtt.publish(topic=self._humidity_topic, message=formatted_humidity)

    def htu_reset(self):
        handle = self._pi.i2c_open(self.bus, self.htu_addr)
        self._pi.i2c_write_byte(handle, self.cmd_reset)
        self._pi.i2c_close(handle)
        time.sleep(0.2)

    def read_temperature(self):
        handle = self._pi.i2c_open(self.bus, self.htu_addr)
        self._pi.i2c_write_byte(handle, self.cmd_rdtemp)
        time.sleep(0.055)
        (count, byteArray) = self._pi.i2c_read_device(handle, 3)
        self._pi.i2c_close(handle)
        t1 = byteArray[0]
        t2 = byteArray[1]
        temp_reading = (t1 * 256) + t2
        temp_reading = math.fabs(temp_reading)
        temperature = ((temp_reading / 65536) * 175.72) - 46.85
        return temperature

    def read_humidity(self):
        handle = self._pi.i2c_open(self.bus, self.htu_addr)
        self._pi.i2c_write_byte(handle, self.cmd_rdhumi)
        time.sleep(0.055)
        (count, byteArray) = self._pi.i2c_read_device(handle, 3)
        self._pi.i2c_close(handle)
        h1 = byteArray[0]
        h2 = byteArray[1]
        humi_reading = (h1 * 256) + h2
        humi_reading = math.fabs(humi_reading)
        uncomp_humidity = ((humi_reading / 65536) * 125) - 6
        temperature = self.read_temperature()
        humidity = ((25 - temperature) * -0.15) + uncomp_humidity
        return humidity
