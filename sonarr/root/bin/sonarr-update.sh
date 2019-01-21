#!/bin/bash

echo "Updating ${APP_NAME}..."

psid="$1"
update_base_path="$2"
full_exec="$3"
exec="$(basename "${full_exec}")"
updated_full_exec=$(find "${update_base_path}" -type f -name "${exec}")
full_update_path="${updated_full_exec%/*}"

if [[ -n "$full_update_path" ]]; then
  rm -rf "/opt/${APP_NAME}/*"
  cp -R "${full_update_path}/*" "/opt/${APP_NAME}/"
  rm -rf "${full_update_path}"
  echo "Restarting ${APP_NAME}"
  sudo s6-svc -t /var/run/s6/services/sonarr
fi
