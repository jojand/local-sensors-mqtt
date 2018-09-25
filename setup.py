#!python

from setuptools import setup, find_packages

setup(
    name='local-sensors MQTT',
    version='0.0.1',
    description='Mqtt gateway locally connected sensors',
    author='Josef Janda',
    author_email='josef.janda@gmail.com',
    license='MIT',
    scripts=[
        'local-sensors-mqtt.py',
    ],
    packages=['components'],
    install_requires=['pigpio', 'paho-mqtt', 'pyyaml', 'w1thermsensor', 'smbus-cffi']
)
