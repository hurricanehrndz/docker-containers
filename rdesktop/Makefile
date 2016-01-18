all: build

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth

ENV_VARS= \
	--env="USER_UID=$(shell id -u)" \
	--env="USER_GID=$(shell id -g)" \
	--env="DISPLAY" \
	--env="XAUTHORITY=${XAUTH}"

VOLUMES= \
	--volume=${XSOCK}:${XSOCK} \
	--volume=${XAUTH}:${XAUTH}

ENV_INSTL_USER=\
	--env="RDESKTOP_USER=${USER}"

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make build            - build the rdesktop image"
	@echo "   2. make install          - install rdesktop wrappers"
	@echo "   3. make rdesktop     - launch rdesktop"
	@echo "   4. make bash             - bash login"
	@echo ""

clean:
	@docker rm -f `docker ps -a | grep "${USER}/rdesktop" | awk '{print $$1}'` > /dev/null 2>&1 || exit 0
	@docker rmi `docker images  | grep "${USER}/rdesktop" | awk '{print $$3}'` > /dev/null 2>&1 || exit 0

build:
	@docker build --rm=true --tag=${USER}/rdesktop .

install uninstall: build
	@docker run -it --rm \
		--volume=/usr/local/bin:/target \
		${ENV_INSTL_USER} \
		${USER}/rdesktop:latest $@

rdesktop bash:
	@touch ${XAUTH}
	@auth nlist :0 | sed -e 's/^..../ffff/' | xauth -f ${XAUTH} nmerge -
	docker run -it --rm \
		${ENV_VARS} \
		${VOLUMES} \
		${USER}/rdesktop:latest $@
