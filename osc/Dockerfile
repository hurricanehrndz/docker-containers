FROM opensuse/amd64:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_US.UTF-8" s6_overlay_version="1.17.2.0" APP_NAME="osc" IMG_NAME="osc" TAG_NAME="latest" S6_LOGGING="1" TERM=xterm-256color

RUN zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in --no-recommends \
	ca-certificates{-cacert,-mozilla} \
	curl \
	git \
	glibc-locale \
	gnome-keyring \
	osc \
	python-gnomekeyring \
	python-keyring \
	tar \
	timezone \
	vim \
	vim-data \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && cd /usr/lib/locale \
  && ls | grep -ve "en_CA*\|en_US*" | xargs rm -rf \
  && cd /usr/share/locale \
  &&  find -name '*.mo' | grep -ve "en_US*" | xargs rm \
  && git clone --depth 1 https://github.com/hurricanehrndz/vim /var/cache/.vim \
  && git clone --depth 1 https://github.com/altercation/vim-colors-solarized /var/cache/.vim/bundle/vim-colors-solarized \
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
	`rpm -qa | grep systemd` \
	curl \
  && ls /usr/lib/locale | grep -ve "en_CA*\|en_US*" | awk '{if(system("[ -f "$1" ]") == 0) {print $1} }' | xargs rm -rf \
  && find /usr/share/locale -type f -name '*.mo' | grep -ve "en_US*"  | awk '{if(system("[ -f "$1" ]") == 0) {print $1} }' | xargs rm \
  && zypper cc --all \
  && rm -rf /usr/share/{man,doc,info,gnome/help} \
  && rm -rf /var/cache/zypp* \
  && rm -rf /tmp/* \
  && rm -rf /var/log/*

COPY root /
ENTRYPOINT ["/entrypoint"]
