#!/usr/bin/make -f

SHELL := /bin/bash
IMG_NAME := "base"
IMG_REPO := "hurricane"

root_repo := "http://download.opensuse.org/repositories/home:/hurricanehernandez:/docker/images/"
qemu_repo := "http://download.opensuse.org/tumbleweed/repo/oss/suse/x86_64"

all: armv7l aarch64 x86_64 end

armv7l: ARCH := armv7l
aarch64: ARCH := aarch64
x86_64: ARCH := x86_64
armv7l aarch64 x86_64:
	@echo "Building $(IMG_NAME) for $(ARCH)"
	$(eval BUILDDIR := /var/tmp/$(IMG_REPO)_$(IMG_NAME)_$(ARCH))
	@if  [[ -d $(BUILDDIR) ]]; then \
		rm -rf $(BUILDDIR); \
	fi
	mkdir -p $(BUILDDIR)
	mkdir -p $(BUILDDIR)/usr/bin
	cp -r overlay-$(ARCH) $(BUILDDIR)/overlay-$(ARCH)
	cp Dockerfile $(BUILDDIR)
	$(eval rootfs_file := $(shell curl -s $(root_repo) --list-only | sed -n s%".*>\(.*${ARCH}.*-.*tar.xz\)</a>.*"%"\1"%p | sort -i | tail -1))
	curl -L $(root_repo)/$(rootfs_file) -o $(BUILDDIR)/rootfs.tar.xz
	@echo "Adding qemu files for $(ARCH)"
	$(eval rpm_name := $(shell curl -s $(qemu_repo)/ --list-only | grep qemu-linux | sed -n s%".*>\(qemu-linux-.*rpm\)</a>.*"%"\1"%p | sort -i | tail -1))
	@if [[ $(ARCH) ==  "armv7l" ]]; then \
		echo "Fetching: $(qemu_repo)/$(rpm_name)"; \
		curl -L $(qemu_repo)/$(rpm_name) -o $(BUILDDIR)/qemu-linux-user.rpm; \
		rpm2cpio $(BUILDDIR)/qemu-linux-user.rpm | cpio -D $(BUILDDIR) -idmv "*qemu-arm" "*qemu-arm-*"; \
	fi
	@if [[ $(ARCH) ==  "aarch64" ]]; then \
		echo "Fetching: $(qemu_repo)/$(rpm_name)"; \
		curl -L $(qemu_repo)/$(rpm_name) -o $(BUILDDIR)/qemu-linux-user.rpm; \
		rpm2cpio $(BUILDDIR)/qemu-linux-user.rpm | cpio -D $(BUILDDIR) -idmv "*qemu-aarch*"; \
	fi
	@if [[ (! -e /proc/sys/fs/binfmt_misc/qemu-arm || \
			! -e /proc/sys/fs/binfmt_misc/qemu-aarch64) \
			&& $(ARCH) != "x86_64" ]]; then \
		echo "Registering qemu binfmt!"; \
		docker run --rm --privileged emby/qemu-register:latest; \
	fi
	cd $(BUILDDIR) && \
		docker build --no-cache=true --build-arg ARCH=$(ARCH) --rm=true --tag=$(IMG_REPO)/$(IMG_NAME):$(ARCH) .
	@if [[ $(ARCH) ==  "x86_64" ]]; then \
		docker tag $(IMG_REPO)/$(IMG_NAME):$(ARCH) $(IMG_REPO)/$(IMG_NAME):latest; \
	fi
	rm -rf $(BUILDDIR)

push:
	docker push $(IMG_REPO)/$(IMG_NAME)

end:
	@echo "Done!"

.PHONY: all armv7l aarch64 x86_64 end
