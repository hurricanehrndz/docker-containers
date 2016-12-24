FROM hurricane/base:ARCH
ENV  APP_NAME="couchpotato" IMG_NAME="couchpotato" TAG_NAME="${ARCH}" S6_LOGGING="0" PYTHONIOENCODING="UTF-8" UMASK=002 EDGE=0

RUN zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in -f --no-recommends \
	ca-certificates{-cacert,-mozilla} \
	curl \
	git-core \
	glibc-locale \
	python \
	python-lxml \
	python-pysqlite \
	python-pyOpenSSL \
	tar \
	timezone \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && mkdir -p /usr/lib/${APP_NAME} \
  && git clone --depth=1 https://github.com/CouchPotato/CouchPotatoServer.git /usr/lib/${APP_NAME} \
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
	tar \
  && ls /usr/lib/locale | grep -ve "en_CA*\|en_US*" | awk '{if(system("[ -f "$1" ]") == 0) {print $1} }' | xargs rm -rf \
  && find /usr/share/locale -type f -name '*.mo' | grep -ve "en_US*"  | awk '{if(system("[ -f "$1" ]") == 0) {print $1} }' | xargs rm \
  && zypper cc --all \
  && rm -rf /usr/share/{man,doc,info,gnome/help} \
  && rm -rf /var/cache/zypp* \
  && rm -rf /tmp/* \
  && rm -rf /var/log/*

COPY root /
ENTRYPOINT ["/init"]
