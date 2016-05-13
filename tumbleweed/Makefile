all: build

IMG_NAME="tumbleweed"
TAG_NAME="latest"

ifndef APP_REPO
APP_REPO=${USER}
endif

build:
	@docker build --rm=true --tag=${APP_REPO}/${IMG_NAME}:${TAG_NAME} .
