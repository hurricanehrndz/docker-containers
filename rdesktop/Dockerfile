FROM opensuse:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_US.UTF-8" s6_overlay_version="1.17.1.2" APP_NAME="rdesktop" IMG_NAME="rdesktop" TAG_NAME="latest" S6_LOGGING="1"

RUN zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in --no-recommends \
	curl \
	tar \
	glibc-locale \
	timezone \
	rdesktop \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && cd /usr/lib/locale \
  && ls | grep -ve "en_CA*\|en_US*" | xargs rm -rf \
  && cd /usr/share/locale \
  &&  find -name '*.mo' | grep -ve "en_US*" | xargs rm \
  && rpm -e --nodeps --allmatches --noscripts \
	tar \
	curl \
	`rpm -qa | grep dbus-1` \
	`rpm -qa | grep pinentry` \
	`rpm -qa | grep openSUSE-release` \
	`rpm -qa | grep perl` \
	`rpm -qa | grep kmod` \
	`rpm -qa | grep kbd` \
	`rpm -qa | grep cryptsetup` \
	`rpm -qa | grep mapper` \
	`rpm -qa | grep pinentry` \
	`rpm -qa | grep qrencode` \
	`rpm -qa | grep cpio` \
	`rpm -qa | grep pigz` \
  && zypper cc --all \
  && rm -rf /usr/share/{man,doc,info,gnome/help} \
  && rm -rf /var/cache/zypp* \
  && rm -rf /tmp/* \
  && rm -rf /var/log/*

COPY root /
ENTRYPOINT ["/init"]
