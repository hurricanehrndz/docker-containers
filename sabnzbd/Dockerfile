FROM hurricane/base:x86_64
ARG ARCH=latest
ENV APP_NAME="sabnzbd" IMG_NAME="sabnzbd" TAG_NAME="${ARCH}" S6_LOGGING="0" PYTHONIOENCODING="UTF-8" UMASK=002 EDGE=0

RUN zypper --non-interactive ar -f -n repo-unrar http://download.opensuse.org/repositories/Archiving/openSUSE_Factory/ repo-unrar \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in -f --no-recommends \
	ca-certificates{-cacert,-mozilla} \
	curl \
	git-core \
	gcc \
	glibc-locale \
	p7zip \
	par \
	python \
	python-Cheetah \
	python-devel \
	python-lxml \
	python-pip \
	python-pyOpenSSL \
	python-pysqlite \
	tar \
	timezone \
	unrar \
	unzip \
  && pip install --upgrade pip \
  && pip install http://www.golug.it/pub/yenc/yenc-0.4.0.tar.gz \
  && zypper rm -y -u --force-resolution gcc python-devel python-pip \
  && mkdir -p /usr/lib/${APP_NAME} \
  && TAG=$(curl -sSL https://github.com/sabnzbd/sabnzbd/tags.atom | sed -n -e '/releases\/tag/{s/.*tag\/\([^"]*\).*/\1/p}' | head -1) \
  && git clone -b "${TAG}" --single-branch --depth 1 https://github.com/sabnzbd/sabnzbd.git /usr/lib/${APP_NAME} \
  && pushd /usr/lib/${APP_NAME} \
  && COMMITSH=$(git rev-list ${TAG}) \
  && popd \
  && sed -i s/"\(__baseline__\s[=]\s\).*"/"\1\"${COMMITSH}\""/ /usr/lib/${APP_NAME}/${APP_NAME}/version.py \
  && sed -i s/"\(__version__\s[=]\s\).*"/"\1\"${TAG}\""/ /usr/lib/${APP_NAME}/${APP_NAME}/version.py \
  && rpm -e --nodeps --allmatches --noscripts \
	`rpm -qa | grep aaa_base` \
	`rpm -qa | grep acl | grep -v lib` \
	`rpm -qa | grep branding-openSUSE` \
	`rpm -qa | grep cpio` \
	`rpm -qa | grep cryptsetup` \
	`rpm -qa | grep dbus-1` \
	`rpm -qa | grep dracut` \
	`rpm -qa | grep fipscheck` \
	`rpm -qa | grep kbd` \
	`rpm -qa | grep kmod` \
	`rpm -qa | grep mapper` \
	`rpm -qa | grep ncurses-utils` \
	`rpm -qa | grep openSUSE-release` \
	`rpm -qa | grep perl` \
	`rpm -qa | grep pigz` \
	`rpm -qa | grep pinentry` \
	`rpm -qa | grep pkg-config` \
	`rpm -qa | grep qrencode` \
	`rpm -qa | grep sg3_utils` \
	`rpm -qa | grep systemd | grep -v lib` \
  && zypper cc --all \
  && rm -rf /usr/share/{man,doc,info,gnome/help} \
  && rm -rf /var/cache/zypp* \
  && rm -rf /tmp/* \
  && rm -rf /var/log/*

COPY root /
VOLUME [ "/config" ]
EXPOSE 8080
ENTRYPOINT ["/init"]
