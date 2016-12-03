#!/bin/bash

echo "Updating ${APP_NAME}..."
UPDATE_SOURCE="$2"
EXEC="$3"
INSTALL_PATH="$(basnename ${EXEC})"
UPDATED_EXEC="$(find ${UPDATE_SOURCE} -type f -name "NzbDrone.exe")"
UPDATE_PATH="$(basename ${UPDATED_EXEC})"


if [[ -n "$UPDATE_PATH" ]]; then
  rm -rf /opt/${APP_NAME}/*
  rm -rf /opt/${APP_NAME}/.*
  cp -R ${UPDATE_PATH}/* /opt/${APP_NAME}/
  cp -R ${UPDATE_PATH}/.* /opt/${APP_NAME}/
  rm -rf ${UPDATE_PATH}
  echo "Restarting ${APP_NAME}"
  sudo s6-svc -t /var/run/s6/services/sonarr
fi
