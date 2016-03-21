FROM opensuse:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_US.UTF-8" s6_overlay_version="1.17.2.0" APP_NAME="irssi" IMG_NAME="irssi" TAG_NAME="latest" S6_LOGGING="0"

RUN zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in --no-recommends \
	bitlbee \
	ca-certificates{-cacert,-mozilla} \
	curl \
	git-core \
	glibc-locale \
	irssi \
	irssi-otr \
	libnotify4 \
	perl \
	perl-base \
	perl-Crypt-Blowfish  \
	perl-Crypt-CBC \
	perl-Crypt-DH-GMP \
	perl-Crypt-OpenSSL-Bignum \
	perl-Text-CharWidth \
	tar \
	timezone \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && cd /usr/lib/locale \
  && ls | grep -ve "en_CA*\|en_US*" | xargs rm -rf \
  && rpm -e --nodeps --allmatches --noscripts \
	`rpm -qa | grep cpio` \
	`rpm -qa | grep cryptsetup` \
	`rpm -qa | grep dbus-1` \
	`rpm -qa | grep kbd` \
	`rpm -qa | grep kmod` \
	`rpm -qa | grep mapper` \
	`rpm -qa | grep openSUSE-release` \
	`rpm -qa | grep pigz` \
	`rpm -qa | grep pinentry` \
	`rpm -qa | grep qrencode` \
	curl \
	tar \
  && git clone --depth 1 https://github.com/irssi/scripts.irssi.org.git /usr/local/share/irssi \
  && git clone --depth 1 https://github.com/huyz/irssi-colors-solarized.git /usr/local/share/irssi/themes/solarized-universal.theme  \
  && zypper cc --all \
  && rm -rf /usr/lib64/gconv/* \
  && rm -rf /usr/share/{man,doc,info,gnome/help} \
  && rm -rf /var/cache/zypp* \
  && rm -rf /tmp/* \
  && rm -rf /var/log/*

COPY root /
ENTRYPOINT ["/init"]
