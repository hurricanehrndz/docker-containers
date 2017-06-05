FROM hurricane/base:x86_64
ARG ARCH
ENV APP_NAME="sonarr" IMG_NAME="sonarr" TAG_NAME="${ARCH}" S6_LOGGING="0" UMASK=0 EDGE=0

RUN zypper --non-interactive ar -f -n repo-mediainfo http://download.opensuse.org/repositories/home:/MediaArea_net:/snapshots/openSUSE_Tumbleweed repo-mediainfo \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive in --no-recommends \
	gettext-runtime \
	libmediainfo0 \
	libzen0 \
	mediainfo \
	mono-core \
	mono-devel \
	sudo \
	timezone \
	zip \
  && mkdir -p /opt/${APP_NAME} \
  && curl -sSL http://update.sonarr.tv/v2/master/mono/NzbDrone.master.tar.gz | tar -C /opt/${APP_NAME} -xzv --strip-components=1 \
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
EXPOSE 8989
ENTRYPOINT ["/init"]
