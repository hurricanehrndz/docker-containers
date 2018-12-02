FROM __BASEIMAGE_ARCH__/debian:stable

ARG DEBIAN_FRONTEND=noninteractive
ENV LC_ALL="en_US.UTF-8" LANG="en_US.UTF-8" APP_NAME="watcher3" IMG_NAME="watcher3" S6_LOGGING="0" UMASK=002 EDGE=0

__CROSS_COPY qemu-__QEMU_ARCH__-static /usr/bin

RUN apt-get update \
 && apt-get -y upgrade \
 && apt-get -qq install -y --no-install-recommends  \
	ca-certificates \
	curl \
	git-core \
	locales \
	python3 \
	tzdata \
 && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen --no-purge en_US.UTF-8 \
 && dpkg-reconfigure --frontend=noninteractive locales \
 && update-locale LANG=en_US.UTF-8 \
 && git clone https://github.com/nosmokingbandit/Watcher3.git /opt/${APP_NAME} \
 && apt-get clean -y \
 && apt-get autoremove -y \
 && rm -rf /tmp/* /var/tmp/* \
 && rm -rf /var/lib/apt/lists/*

COPY root /
VOLUME [ "/config" "/opt/$APP_NAME/userdata"]
EXPOSE 9090
ENTRYPOINT ["/init"]
