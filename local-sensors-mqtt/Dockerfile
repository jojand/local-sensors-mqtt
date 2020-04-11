FROM debian:stretch

RUN apt-get update && \
  apt-get install -y git build-essential python-dev python-smbus python-pip libssl-dev libffi-dev && \
  apt-get clean

COPY ./components /build/components
COPY ./resources /build/resources
COPY ./local-sensors-mqtt.py /build/local-sensors-mqtt.py
COPY ./setup.py /build/setup.py
WORKDIR /build
RUN git clone https://github.com/adafruit/Adafruit_Python_BMP.git && \
    cd Adafruit_Python_BMP && \
    python setup.py install
RUN cd /build && python setup.py install
    
CMD local-sensors-mqtt
