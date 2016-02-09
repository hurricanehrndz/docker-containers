all: build

APP_NAME="google-chrome"
IMG_NAME="google-chrome"
TAG_NAME="latest"

ifndef APP_REPO
APP_REPO=${USER}
endif

ENV_VARS= \
    --env="APP_REPO=${APP_REPO}" \
    --env="APP_USER=${USER}" \
	--env="APP_UID=$(shell id -u)" \
	--env="APP_GID=$(shell id -g)" \
    --env="IMG_NAME=${IMG_NAME}" \
    --env="TAG_NAME=${TAG_NAME}"


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
	@docker rm -f `docker ps -a | grep "${APP_REPO}/${IMG_NAME}" | awk '{print $$1}'` > /dev/null 2>&1 || exit 0
	@docker rmi `docker images  | grep -e "${APP_REPO}/${IMG_NAME}.*${TAG_NAME}" | awk '{print $$3}'` > /dev/null 2>&1 || exit 0

build:
	@docker build --rm=true --tag=${APP_REPO}/${IMG_NAME}:${TAG_NAME} .

instl uninstl: build
	@docker run -it --rm \
		--volume=/usr/local/bin:/target \
		${ENV_VARS} \
		${APP_REPO}/${APP_NAME}:${TAG_NAME} $@

service: build
	@docker run -it --rm \
		--volume=/etc/systemd/system:/target \
		${ENV_VARS} \
		${APP_REPO}/${APP_NAME}:${TAG_NAME} instl service
