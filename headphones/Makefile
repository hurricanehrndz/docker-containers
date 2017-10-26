#!/usr/bin/make -f

SHELL := /bin/bash
IMG_NAME := headphones
IMG_REPO := hurricane

.PHONY: all armv7l aarch64 x86_64 end
all: armv7l aarch64 x86_64 end

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
	sed -i -e s%"\(base[:]\).*"%"\1$(ARCH)"% $(BUILDDIR)/Dockerfile
	@if [[ $(ARCH) !=  "x86_64" ]]; then \
		if [[ (! -e /proc/sys/fs/binfmt_misc/qemu-arm || ! -e /proc/sys/fs/binfmt_misc/qemu-aarch64) ]]; then \
			echo "Registering qemu binfmt!"; \
			docker run --rm --privileged emby/qemu-register:latest; \
		fi; \
		sed -i -e s%"\(ffmpeg-release-\)64\(bit-static.tar.xz\)"%"\1armhf-32\2"% $(BUILDDIR)/Dockerfile; \
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
