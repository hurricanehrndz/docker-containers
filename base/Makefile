#!/usr/bin/make -f

SHELL := /bin/bash
IMG_NAME := "base"
IMG_REPO := "hurricane"

repo := "http://download.opensuse.org/repositories/home:/hurricanehernandez:/docker/images/"
all: armv7l aarch64 x86_64
.PHONY: all armv7l aarch64 x86_64 end

armv7l: ARCH := "armv7l"
aarch64: ARCH := "aarch64"
x86_64: ARCH := "x86_64"
armv7l aarch64 x86_64:
	@echo "Building $(ARCH)"
	$(eval rootfs_file := $(shell curl -s $(repo) --list-only | sed -n s%".*>\(.*${ARCH}.*-.*tar.xz\)</a>.*"%"\1"%p | sort -i | head -1))
	curl -L $(repo)/$(rootfs_file) -o rootfs.tar.xz
	docker build --build-arg ARCH=$(ARCH) --rm=true --tag=$(IMG_REPO)/$(IMG_NAME):$(ARCH) .
	docker push $(IMG_REPO)/$(IMG_NAME):$(ARCH)
	rm rootfs.tar.xz

end:
	@echo "Done!"
