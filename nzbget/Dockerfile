FROM hurricane/base:x86_64
ARG ARCH
ENV APP_NAME="nzbget" IMG_NAME="nzbget" TAG_NAME="${ARCH}" S6_LOGGING="0" PYTHONIOENCODING="UTF-8" UMASK=002 EDGE=0

RUN zypper --non-interactive ar -f -n repo-unrar http://download.opensuse.org/repositories/Archiving/openSUSE_Factory/ repo-unrar \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive in --no-recommends \
	ca-certificates{-cacert,-mozilla} \
	curl \
	git-core \
	glibc-locale \
	p7zip \
	python \
	tar \
	timezone \
	unrar \
	unzip \
  && mkdir -p /usr/lib/${APP_NAME} \
  && curl -o /tmp/nzbget-linux.run -sSL $(curl -sSL http://nzbget.net/info/nzbget-version-linux.json | sed -n "s/^.*stable-download.*: \"\(.*\)\".*/\1/p") \
  && sh /tmp/nzbget-linux.run --destdir /usr/lib/${APP_NAME} \
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
EXPOSE 6789
ENTRYPOINT ["/init"]
