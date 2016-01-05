#!/bin/bash
set -e

USER_UID=${USER_UID:-1000}
USER_GID=${USER_GID:-1000}
MUTT_USER=${MUTT_USER:-mutt}
MUTT_REPO=${MUTT_REPO:-hurricane}

install_mutt() {
	echo "Installing mutt..."
	install -m 0755 /var/cache/mutt/mutt /target/
	if [ "${MUTT_USER}" != "mutt" ] && [ -n "${MUTT_USER}" ]; then
		echo "Updating user to ${MUTT_USER}..."
		sed -i -e s%"-mutt"%"-${MUTT_USER}"%1 /target/mutt
	fi
	sed -i -e s%"\(MUTT_REPO=\).*$"%"\1${MUTT_REPO}"%1 /target/mutt
}

uninstall_mutt() {
	echo "Uninstalling mutt..."
	rm -rf /target/mutt
}

create_user() {
	# ensure home directory is owned by user
	# and that the profile files exist
	if [[ -d /home/${MUTT_USER} ]]; then
		chown ${USER_UID}:${USER_GID} /home/${MUTT_USER}
		# copy user files from /etc/skel
		cp /etc/skel/.bashrc /home/${MUTT_USER}
		cp /etc/skel/.bash_logout /home/${MUTT_USER}
		cp /etc/skel/.profile /home/${MUTT_USER}
		cp -R /var/cache/mutt/.mutt /home/${MUTT_USER}/
		cp -R /var/cache/.vim /home/${MUTT_USER}/
		cp -R /var/cache/.config /home/${MUTT_USER}/
		mkdir -p /home/${MUTT_USER}/.mutt/temp

		# edit profile, to auto start and setup mutt
		cat <<- EOF >> /home/${MUTT_USER}/.profile
		trap exit 2
		# Invoke GnuPG-Agent the first time we login.
		export GPG_AGENT_INFO=${GPG_AGENT_INFO}
		GPG_TTY=$(tty)
		export GPG_TTY

		# Setup and start mutt
		echo " " | gpg --no-tty --use-agent -q -r ${GPGKEY} -ae | gpg --no-tty --use-agent -q
		echo "Setting up mutt with secrets."
		python /var/cache/muttbot/muttbot.py -c /home/${MUTT_USER}/.muttinfo
		EOF

		cat <<- EOF >> /home/${MUTT_USER}/.muttinfo
		#!/bin/sh
		gpg --no-tty --use-agent -q -d /home/${MUTT_USER}/.muttsecrets
		EOF

		# change profile permission to mutt user
		chown -R ${USER_UID}:${USER_GID} \
		/home/${MUTT_USER}/.bashrc \
		/home/${MUTT_USER}/.profile \
		/home/${MUTT_USER}/.bash_logout \
		/home/${MUTT_USER}/.mutt \
		/home/${MUTT_USER}/.muttinfo \
		/home/${MUTT_USER}/.vim \
		/home/${MUTT_USER}/.config

		chmod +x /home/${MUTT_USER}/.muttinfo
	fi
	# create group with USER_GID
	if ! getent group ${MUTT_USER} >/dev/null; then
		groupadd -f -g ${USER_GID} ${MUTT_USER} > /dev/null 2>&1
	fi
	# create user with USER_UID
	if ! getent passwd ${MUTT_USER} >/dev/null; then
		adduser --disabled-login --uid ${USER_UID} --gid ${USER_GID} \
			--gecos 'Containerized App User' ${MUTT_USER} > /dev/null 2>&1
	fi
}

launch_mutt() {
	echo "Starting mutt for user ${MUTT_USER}."
	[ ! -d /home/${MUTT_USER}/.gnupg ] && \
		echo "Error: user's gnupg directory not mounted within container." && \
		exit 1
	if [ ! -f /home/${MUTT_USER}/.muttsecrets ]; then
		echo "File .muttsecrets does not exist in home."
		echo "Please create and encrypt with your gpg."
		exit 1
	fi
	exec sudo --login --set-home --preserve-env -u ${MUTT_USER}
}

case "$1" in
	install)
		install_mutt
		;;
	uninstall)
		uninstall_mutt
		;;
	mutt)
		create_user
		launch_mutt $@
		;;
	*)
		create_user
		exec $@
		;;
esac
