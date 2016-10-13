FROM opensuse/amd64:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_US.UTF-8" s6_overlay_version="1.18.1.5" APP_NAME="znc" IMG_NAME="znc" TAG_NAME="latest" S6_LOGGING="0"

RUN zypper --non-interactive ar -f -n Personal-Repo http://download.opensuse.org/repositories/home:/hurricanehernandez/openSUSE_Tumbleweed/ repo-hurricane \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in --no-recommends \
	automake \
	bitlbee \
	ca-certificates{-cacert,-mozilla} \
	curl \
	gcc-c++ \
	glibc-locale \
	libicu-devel \
	libicu57_1 \
	libopenssl1_0_0 \
	libopenssl-devel \
	libpurple \
	libpurple-plugin-hangouts \
	make \
	psmisc \
	tar \
	telegram-purple \
	timezone \
	znc \
	znc-devel \
	znc-perl \
	znc-python3 \
	znc-tcl \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && curl -sLO https://raw.githubusercontent.com/jreese/znc-push/master/push.cpp \
  && znc-buildmod push.cpp \
  && cp push.so /usr/lib64/znc/push.so \
  && curl -sLO https://raw.githubusercontent.com/kylef/znc-contrib/master/clientaway.cpp \
  && znc-buildmod clientaway.cpp \
  && cp clientaway.so /usr/lib64/znc/clientaway.so \
  && rpm -e --nodeps --allmatches --noscripts \
	`rpm -qa | grep aaa_base` \
	`rpm -qa | grep acl | grep -v lib` \
	`rpm -qa | grep branding-openSUSE` \
	`rpm -qa | grep cpio` \
	`rpm -qa | grep cryptsetup` \
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
	libicu-devel \
	libopenssl-devel \
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
