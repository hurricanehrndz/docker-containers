all: build

APP_NAME="mutt"
APP_REPO=${USER}

ENV_VARS= \
	--env="APP_REPO=${APP_REPO}" \
	--env="APP_USER=${USER}"

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make build            - build the ${APP_NAME} image"
	@echo "   2. make install          - install ${APP_NAME} wrappers"
	@echo "   3. make ${APP_NAME}      - launch ${APP_NAME}"
	@echo "   4. make bash             - bash login"
	@echo ""

clean:
	@docker rm -f `docker ps -a | grep "${APP_REPO}/${APP_NAME}" | awk '{print $$1}'` > /dev/null 2>&1 || exit 0
	@docker rmi `docker images  | grep "${APP_REPO}/${APP_NAME}" | awk '{print $$3}'` > /dev/null 2>&1 || exit 0

build:
	@docker build --rm=true --tag=${APP_REPO}/${APP_NAME} .

instl uninstl: build
	@docker run -it --rm \
		--volume=/usr/local/bin:/target \
		${ENV_VARS} \
		${APP_REPO}/${APP_NAME}:latest $@

${APP_NAME} bash:
	@touch ${XAUTH}
	@auth nlist :0 | sed -e 's/^..../ffff/' | xauth -f ${XAUTH} nmerge -
	@docker run -it --rm \
		${ENV_VARS} \
		${VOLUMES} \
		${APP_REPO}/${APP_NAME}:latest $@
