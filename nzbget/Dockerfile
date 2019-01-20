FROM __BASEIMAGE_ARCH__/debian:stable

ARG DEBIAN_FRONTEND=noninteractive
ENV LC_ALL="en_US.UTF-8" LANG="en_US.UTF-8" APP_NAME="nzbget" IMG_NAME="nzbget" S6_LOGGING="0" UMASK=002 EDGE=0

__CROSS_COPY qemu-__QEMU_ARCH__-static /usr/bin

RUN apt-get update \
 && apt-get -y upgrade \
 && apt-get -qq install -y --no-install-recommends  $(apt-cache depends nzbget | awk '/Depends:/{printf "%s ",$2}') \
 && apt-get -qq install -y --no-install-recommends  \
	ca-certificates \
	curl \
	locales \
	par2 \
	python \
	python-pip \
	python3 \
	python3-pip \
	tzdata \
 && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen --no-purge en_US.UTF-8 \
 && dpkg-reconfigure --frontend=noninteractive locales \
 && update-locale LANG=en_US.UTF-8 \
 && mkdir -p /usr/lib/${APP_NAME} \
 && curl -o /tmp/nzbget-linux.run -ksSL $(curl -sSL http://nzbget.net/info/nzbget-version-linux.json | sed -n "s/^.*stable-download.*: \"\(.*\)\".*/\1/p") \
 && sh /tmp/nzbget-linux.run --destdir /usr/lib/${APP_NAME} \
 && ln -sf /usr/lib/${APP_NAME}/unrar /usr/bin/unrar \
 && ln -sf /usr/lib/${APP_NAME}/7za /usr/bin/7za \
 && apt-get clean -y \
 && apt-get autoremove -y \
 && rm -rf /tmp/* /var/tmp/* \
 && rm -rf /var/lib/apt/lists/*

COPY root /
VOLUME [ "/config" ]
EXPOSE 6789
ENTRYPOINT ["/init"]
