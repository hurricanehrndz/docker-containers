#!/usr/bin/make -f

SHELL := /bin/bash
IMG_NAME := sonarr
IMG_REPO := hurricane

.PHONY: all armv7l aarch64 x86_64 end
all: armv7l aarch64 x86_64

armv7l: ARCH := armv7l
aarch64: ARCH := aarch64
x86_64: ARCH := x86_64
armv7l aarch64 x86_64:
	@ echo "Building $(IMG_NAME) for $(ARCH)"
	$(eval BUILDDIR := /var/tmp/$(IMG_REPO)_$(IMG_NAME)_$(ARCH))
	@ if  [[ -d $(BUILDDIR) ]]; then \
		rm -rf $(BUILDDIR); \
	fi
	mkdir -p $(BUILDDIR)
	cp Dockerfile $(BUILDDIR)
	cp -r root $(BUILDDIR)/
	sed -i s'/\(base[:]\).*/\1$(ARCH)/' $(BUILDDIR)/Dockerfile
	@if [[ $(ARCH) !=  "x86_64" ]]; then \
		sed -i '/repo-mediainfo/s/openSUSE_Tumbleweed/openSUSE_Factory_ARM/' /var/tmp/$(IMG_NAME)_$(ARCH)/Dockerfile; \
		if [[ (! -e /proc/sys/fs/binfmt_misc/qemu-arm || ! -e /proc/sys/fs/binfmt_misc/qemu-aarch64) ]]; then \
			echo "Registering qemu binfmt!"; \
			docker run --rm --privileged emby/qemu-register:latest; \
		fi \
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
