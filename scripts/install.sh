#!/bin/bash

if [[ ${1} == "" ]]; then
    echo "usage: ${0} installation-destination"
fi

PROJECT_NAME="local-sensors-mqtt"
INSTALLATION_DESTINATION=${1}
VIRTUAL_ENV="local-sensors-mqtt-venv"
SERVICE_SCRIPT="${PROJECT_NAME}.service"
LOG_DIR="/var/log/${PROJECT_NAME}"

# prepare virtualenv
mkdir -p ${INSTALLATION_DESTINATION}
virtualenv -p python ${INSTALLATION_DESTINATION}
source ${INSTALLATION_DESTINATION}/bin/activate

python setup.py install

# config file
mkdir -p ${INSTALLATION_DESTINATION}/resources
cp resources/configuration.yml ${INSTALLATION_DESTINATION}/resources/configuration.yml

# log file
mkdir -p ${LOG_DIR}

# setup a service
cat > /etc/systemd/system/${SERVICE_SCRIPT} << END
[Unit]
Description=Local sensors - MQTT
After=network.target

[Service]
Restart=always
RestartSec=3
Type=simple
ExecStart=${INSTALLATION_DESTINATION}/bin/${PROJECT_NAME}.py -c ${INSTALLATION_DESTINATION}/resources/configuration.yml -l ${LOG_DIR}/${PROJECT_NAME}.log

[Install]
WantedBy=multi-user.target

END

chmod 755 /etc/systemd/system/${SERVICE_SCRIPT}
systemctl daemon-reload
systemctl enable ${SERVICE_SCRIPT}
