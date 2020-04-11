#!/bin/bash

if [[ ${1} == "" ]]; then
    echo "usage: ${0} installation-destination"
    exit 1
fi

PROJECT_NAME="local-sensors-mqtt"
INSTALLATION_DESTINATION=${1}
SERVICE_SCRIPT="${PROJECT_NAME}.service"

echo "disabling service ... "
systemctl disable ${SERVICE_SCRIPT}
echo "stopping service ... "
systemctl stop ${SERVICE_SCRIPT}
echo "removing files ... "
rm -rf ${INSTALLATION_DESTINATION}
echo "removing service script ... "
rm -rf /etc/systemd/system/${SERVICE_SCRIPT}
