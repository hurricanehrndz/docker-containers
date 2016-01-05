all: build

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth

ENV_VARS= \
	--env="USER_UID=$(shell id -u)" \
	--env="USER_GID=$(shell id -g)" \
    --env="DISPLAY" \
    --env="XAUTHORITY=${XAUTH}"

VOLUMES = \
    --volume=${XSOCK}:${XSOCK} \
    --volume=${XAUTH}:${XAUTH}

ENV_INSTL_USER=\
	--env="MUTT_USER=${USER}" \
	--env="MUTT_REPO=${USER}"

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make build            - build the mutt image"
	@echo "   2. make install          - install mutt wrapper"
	@echo "   3. make mutt             - launch mutt"
	@echo "   4. make bash             - bash login"
	@echo ""

clean:
	@docker rm -f `docker ps -a | grep "${USER}/mutt" | awk '{print $$1}'` > /dev/null 2>&1 || exit 0
	@docker rmi `docker images  | grep "${USER}/mutt" | awk '{print $$3}'` > /dev/null 2>&1 || exit 0

build:
	@docker build --rm=true --tag=${USER}/mutt .

install uninstall: build
	@docker run -it --rm \
		--volume=/usr/local/bin:/target \
		${ENV_INSTL_USER} \
		${USER}/mutt:latest $@

mutt bash:
	@touch ${XAUTH}
	@xauth nlist :0 | sed -e 's/^..../ffff/' | xauth -f ${XAUTH} nmerge -
	docker run -it --rm \
		${ENV_VARS} \
		${VOLUMES} \
		${USER}/mutt:latest $@
