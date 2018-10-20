FROM __BASEIMAGE_ARCH__/ubuntu:rolling

ARG DEBIAN_FRONTEND=noninteractive
ENV LC_ALL="en_US.UTF-8" LANG="en_US.UTF-8" APP_NAME="template" IMG_NAME="template" S6_LOGGING="0" UMASK=002 EDGE=0

__CROSS_COPY qemu-__QEMU_ARCH__-static /usr/bin

RUN apt-get update \
 && apt-get -qq install -y --no-install-recommends  \
	ca-certificates \
	curl \
	locales \
	tzdata \
 && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen --no-purge en_US.UTF-8 \
 && dpkg-reconfigure --frontend=noninteractive locales \
 && update-locale LANG=en_US.UTF-8 \
 && apt-get clean -y \
 && apt-get autoremove -y \
 && rm -rf /tmp/* /var/tmp/* \
 && rm -rf /var/lib/apt/lists/*

COPY root /
VOLUME [ "/config" ]
ENTRYPOINT ["/init"]
