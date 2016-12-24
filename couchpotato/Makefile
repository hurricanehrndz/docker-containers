#!/usr/bin/make -f

SHELL := /bin/bash
IMG_NAME := "couchpotato"
IMG_REPO := "hurricane"

repo := "http://download.opensuse.org/tumbleweed/repo/oss/suse/x86_64"
all: armv7l aarch64 x86_64
.PHONY: all armv7l aarch64 x86_64 end

x86_64: ARCH := "x86_64"
x86_64:
	@echo "Building $(ARCH)"
	@ if  [[ -d /var/tmp/$(IMG_NAME)_$(ARCH) ]]; then \
		rm -rf /var/tmp/$(IMG_NAME)_$(ARCH); \
	  fi
	mkdir -p /var/tmp/$(IMG_NAME)_$(ARCH)
	cp Dockerfile /var/tmp/$(IMG_NAME)_$(ARCH)/
	cp -R root /var/tmp/$(IMG_NAME)_$(ARCH)/
	pushd /var/tmp/$(IMG_NAME)_$(ARCH)/
	sed -i '/\(base[:]\).*/\1$(ARCH)/' Dockerfile
	docker build --build-arg ARCH=$(ARCH) --rm=true --tag=$(IMG_REPO)/$(IMG_NAME):$(ARCH) .
	popd
	rm -rf /var/tmp/$(IMG_NAME)*

armv7l: ARCH := "armv7l"
aarch64: ARCH := "aarch64"
armv7l aarch64:
	@ echo "Building ffmpeg for $(ARCH)"
	@ if  [[ -d /var/tmp/$(IMG_NAME)_$(ARCH) ]]; then \
		rm -rf /var/tmp/$(IMG_NAME)_$(ARCH); \
	  fi
	mkdir -p /var/tmp/$(IMG_NAME)_$(ARCH)
	cp Dockerfile /var/tmp/$(IMG_NAME)_$(ARCH)/
	cp -R root /var/tmp/$(IMG_NAME)_$(ARCH)/
	pushd /var/tmp/$(IMG_NAME)_$(ARCH)/
	sed -i '/\(base[:]\).*/\1$(ARCH)/' Dockerfile
	$(eval rpm_name := $(shell curl -s $(repo)/ --list-only | grep qemu-linux | sed -n s%".*>\(qemu-linux-.*rpm\)</a>.*"%"\1"%p))
	curl -L $(repo)/$(rpm_name) -o qemu-linux-user.rpm
	@ if [[ $(ARCH) ==  "armv7l" ]]; then \
		rpm2cpio qemu-linux-user.rpm | cpio -idmv "*qemu-arm*"; \
	  fi
	@ if [[ $(ARCH) ==  "aarch64" ]]; then \
		rpm2cpio qemu-linux-user.rpm | cpio -idmv "*qemu-aarch*"; \
	  fi
	sed -i '/ENV/,/RUN/ {s/^$/COPY usr \/usr/}' Dockerfile
	@ if [[ -d "/proc/sys/fs/binfmt_misc/" ]]; then \
		if [[ "enabled" != $(shell cat /proc/sys/fs/binfmt_misc/status) ]]; then \
			docker run --rm --privileged emby/qemu-builder:register; \
		else \
			docker run --rm --privileged emby/qemu-builder:register -r; \
			docker run --rm --privileged emby/qemu-builder:register; \
		fi \
	  else \
			docker run --rm --privileged emby/qemu-builder:register; \
	  fi
	docker build --build-arg ARCH=$(ARCH) --rm=true --tag=$(IMG_REPO)/$(IMG_NAME):$(ARCH) .
	popd
	rm -rf /var/tmp/$(IMG_NAME)*

end:
	@echo "Done!"
