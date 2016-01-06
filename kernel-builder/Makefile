all: build kernel

current_dir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VOLUMES = \
		  --volume=$(current_dir):/data

VERSION=4.4-rc8

ENV_VARS = \
		   --env="VERSION=${VERSION}"

ifdef PKGVERSION
ENV_VARS += \
			--env="PKGVERSION=${PKGVERSION}"
else
ENV_VARS += \
			--env="PKGVERSION=${VERSION}-1"
endif

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make build            - build kernel-builder docker image"
	@echo "   2. make kernel           - build kernel verison: ${VERSION} with default config"
	@echo "   3. make config-kernel    - run interactive menuconifg and build kernel verison: ${VERSION}"
	@echo ""

clean:
	@docker rm -f `docker ps -a | grep "kernel-builder" | awk '{print $$1}'` > /dev/null 2>&1 || exit 0

build: clean
	@docker build --rm -t ${USER}/kernel-builder .

kernel: build
	@echo "Package will be in ${current_dir}"
	@docker run  \
		${ENV_VARS} \
		${VOLUMES} \
		${USER}/kernel-builder:latest

config-kernel: build
	@echo "Package will be in ${current_dir}"
	@docker run  -it \
		${ENV_VARS} \
		${VOLUMES} \
		${USER}/kernel-builder:latest
