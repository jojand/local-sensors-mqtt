import paho.mqtt.client as mqtt
import logging

class Mqtt:

    KEEPALIVE = 60

    def __init__(self, default_prefix, mqtt_host, mqtt_port=1883):
        self.default_prefix = default_prefix
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqttc = mqtt.Client()
        self.mqttc.connect(host=self.mqtt_host, port=self.mqtt_port, keepalive=self.KEEPALIVE)
        self.mqttc.loop_start()

    def publish(self, topic, message):
        topic = "{}/{}".format(self.default_prefix, topic)
        logging.info("Publishing topic: {}, message: {}".format(topic, message))
        self.mqttc.publish(topic, message)

    def disconnect(self):
        self.mqttc.disconnect()
