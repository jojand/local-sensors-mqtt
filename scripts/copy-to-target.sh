#!/bin/sh

HOST=${1}
PORT=${2}
USER="pi"
REMOTE_PROJECT_PATH="~/development/python/local-sensors-mqtt"

FILES_TO_COPY="${FILES_TO_COPY} *.py"
FILES_TO_COPY="${FILES_TO_COPY} requirements.txt"
FILES_TO_COPY="${FILES_TO_COPY} scripts/install.sh"
FILES_TO_COPY="${FILES_TO_COPY} scripts/uninstall.sh"
FILES_TO_COPY="${FILES_TO_COPY} resources/*.yml"
FILES_TO_COPY="${FILES_TO_COPY} components/*"

echo "copy to target $USER@$HOST:$PORT"

# prepare target folder
echo "preparing remote directory ..."
ssh -p $PORT $USER@$HOST mkdir -p ${REMOTE_PROJECT_PATH}
ssh -p $PORT $USER@$HOST mkdir -p ${REMOTE_PROJECT_PATH}/resources
ssh -p $PORT $USER@$HOST mkdir -p ${REMOTE_PROJECT_PATH}/components
ssh -p $PORT $USER@$HOST mkdir -p ${REMOTE_PROJECT_PATH}/scripts

for file_to_copy in ${FILES_TO_COPY}
do
    echo "copying ${file_to_copy} ..."
    scp -P $PORT ${file_to_copy} ${USER}@${HOST}:${REMOTE_PROJECT_PATH}/${file_to_copy}
done
