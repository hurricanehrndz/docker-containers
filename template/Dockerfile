FROM opensuse:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_CA.UTF-8" s6_overlay_version="1.17.1.1" app_name="template"

RUN zypper --gpg-auto-import-keys ref \
 && zypper up \
 && zypper --non-interactive in --no-recommends \
	curl \
	tar \
	timezone \
 && curl -sL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
 && tar zxf /tmp/s6-overlay-amd64.tar.gz -C / \
 && rm -rf /tmp/* \
 && cd /usr/lib/locale \
 && ls | grep -ve "en_CA*\|en_US*" | xargs rm -rf \
 && cd /usr/share/locale \
 &&  find -name '*.mo' | grep -ve "en_US*" | xargs rm \
 && rpm -e --nodeps --allmatches --noscripts \
	aaa_base \
	dbus-1 \
	dracut \
	kbd \
	kmod \
	ncurses-utils \
	pkg-config \
	sg3_utils \
	systemd \
	systemd-presets-branding-openSUSE \
	systemd-sysvinit \
	tar \
	curl \
	git-core \
	udev \
 && zypper cc --all \
 && rm -rf /var/cache/zypp* \
 && rm -rf /var/log/*

COPY root /
ENTRYPOINT ["/init"]
