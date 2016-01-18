#!/bin/bash
set -e

USER_UID=${USER_UID:-1000}
USER_GID=${USER_GID:-1000}
RDESKTOP_USER=${RDESKTOP_USER:-rdesktop}

install_rdesktop() {
  echo "Installing rdesktop..."
  install -m 0755 /var/cache/rdesktop/rdesktop /target/
  if [ "${RDESKTOP_USER}" != "rdesktop" ] && [ -n "${RDESKTOP_USER}" ]; then
    echo "Updating user to ${RDESKTOP_USER}..."
    sed -i -e s%"-rdesktop"%"-${RDESKTOP_USER}"%1 /target/rdesktop
  fi
  if [[ -n "${RDESKTOP_DATA}" ]]; then
    echo "Updating user volumes..."
    sed -i -e s%"RDESKTOP_DATA=.*$"%"RDESKTOP_DATA\=${RDESKTOP_DATA}"% \
    /target/rdesktop
  fi
}

uninstall_rdesktop() {
  echo "Uninstalling rdesktop wrapper..."
  rm -rf /target/rdesktop-wrapper
  echo "Uninstalling rdesktop..."
  rm -rf /target/rdesktop
}

create_user() {
  # ensure home directory is owned by user
  # and that the profile files exist
  if [[ -d /home/${RDESKTOP_USER} ]]; then
    chown ${USER_UID}:${USER_GID} /home/${RDESKTOP_USER}
    # copy user files from /etc/skel
    cp /etc/skel/.bashrc /home/${RDESKTOP_USER}
    cp /etc/skel/.bash_logout /home/${RDESKTOP_USER}
    cp /etc/skel/.profile /home/${RDESKTOP_USER}
    chown ${USER_UID}:${USER_GID} \
    /home/${RDESKTOP_USER}/.bashrc \
    /home/${RDESKTOP_USER}/.profile \
    /home/${RDESKTOP_USER}/.bash_logout
  fi
  # create group with USER_GID
  if ! getent group ${RDESKTOP_USER} >/dev/null; then
    groupadd -f -g ${USER_GID} ${RDESKTOP_USER} 2> /dev/null
  fi
  # create user with USER_UID
  if ! getent passwd ${RDESKTOP_USER} >/dev/null; then
    adduser --disabled-login --uid ${USER_UID} --gid ${USER_GID} \
      --gecos 'Containerized App User' ${RDESKTOP_USER}
  fi
}

launch_rdesktop() {
  exec sudo -HEu ${RDESKTOP_USER} $@ ${extra_opts}
}

case "$1" in
  install)
    install_rdesktop
    ;;
  uninstall)
    uninstall_rdesktop
    ;;
  rdesktop)
    create_user
    launch_rdesktop $@
    ;;
  *)
    exec $@
    ;;
esac
