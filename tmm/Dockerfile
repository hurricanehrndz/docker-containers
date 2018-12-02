FROM __BASEIMAGE_ARCH__/debian:stable

__CROSS_COPY qemu-__QEMU_ARCH__-static /usr/bin

ARG DEBIAN_FRONTEND=noninteractive
ENV LC_ALL="en_US.UTF-8" LANG="en_US.UTF-8" APP_NAME="tmm" IMG_NAME="tmm" S6_LOGGING="0" UMASK=002 EDGE=0

RUN apt-get update \
 && apt-get -y upgrade \
 && apt-get -qq install -y --no-install-recommends  \
	ca-certificates \
	curl \
	gawk \
	git-core \
	libmediainfo0v5 \
	locales \
	openjdk-8-jdk \
	python3 \
	python3-pip \
	python3-setuptools \
 && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen --no-purge en_US.UTF-8 \
 && dpkg-reconfigure --frontend=noninteractive locales \
 && update-locale LANG=en_US.UTF-8 \
 && pip3 install git+https://github.com/hurricanehrndz/tmm-xmlrpc.git \
 && mkdir -p /opt/${APP_NAME} \
 && rel_url="http://release.tinymediamanager.org/download.php" \
 && rel=$( curl -L "$rel_url" | awk /linux.tar/'{gsub("<a href=\"",""); gsub("\".*$",""); print}') \
 && download_url="http://release.tinymediamanager.org/$rel" \
 && tmm_file="/tmp/tmm.tgz" \
 && curl -o $tmm_file -L $download_url \
 && tar -xvf "$tmm_file" -C /opt/${APP_NAME} \
 && apt-get clean -y \
 && apt-get autoremove -y \
 && rm -rf /tmp/* /var/tmp/* /tmp/tmm \
 && rm -rf /var/lib/apt/lists/* \
 && cd


COPY root /
VOLUME [ "/opt/tmm/data", "/opt/tmm/cache", "/opt/tmm/backup", "/opt/tmm/logs" ]
EXPOSE 8000
ENTRYPOINT ["/init"]
