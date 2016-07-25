#FROM opensuse/amd64:tumbleweed
FROM opensuse:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_US.UTF-8" s6_overlay_version="1.18.1.3" APP_NAME="mutt" IMG_NAME="mutt" TAG_NAME="latest" S6_LOGGING="1" TERM=xterm-256color

RUN zypper --non-interactive addrepo http://download.opensuse.org/repositories/home:hurricanehernandez/openSUSE_Tumbleweed/home:hurricanehernandez.repo \
 && zypper --non-interactive addrepo http://download.opensuse.org/repositories/server:mail/openSUSE_Tumbleweed/server:mail.repo \
 && zypper --non-interactive addrepo http://download.opensuse.org/repositories/home:AndnoVember:test/openSUSE_Factory/home:AndnoVember:test.repo \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive dup \
 && zypper --non-interactive in --no-recommends \
	adwaita-icon-theme \
	ca-certificates{,-cacert,-mozilla} \
	curl \
	dbus-1-x11 \
	dejavu-fonts \
	git-core \
	glibc-i18ndata \
	glibc-locale \
	hicolor-icon-theme \
	home_hurricanehernandez:mutt-kz \
	isync \
	java-1_9_0-openjdk-headless \
	krb5-mini \
	libcrypto38 \
	libgpgme11 \
	libgtk-2_0-0 \
	libidn11 \
	libnotmuch4 \
	libsasl2-3 \
	libslang2 \
	libssl39 \
	libtokyocabinet9 \
	mirage \
	msmtp \
	notmuch \
	pinentry-gtk2 \
	python \
	python-pyinotify \
	python-base \
	python-pip \
	python-PyYAML \
	tar \
	timezone \
	vim-data \
	vim-enhanced \
	w3m \
	zathura \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && curl -skL http://sourceforge.net/projects/davmail/files/davmail/4.7.2/davmail-linux-x86_64-4.7.2-2427.tgz -o /tmp/davmail.tgz \
  && mkdir -p /usr/lib/davmail \
  && tar xf /tmp/davmail.tgz --strip-components=1  -C /usr/lib/davmail/ \
  && git clone --depth 1 https://github.com/hurricanehrndz/vim /var/cache/.vim \
  && git clone --depth 1 https://github.com/dbeniamine/vim-mail /var/cache/.vim/bundle/vim-mail \
  && git clone --depth 1 https://github.com/altercation/vim-colors-solarized /var/cache/.vim/bundle/vim-colors-solarized \
  && pip install --upgrade pip \
  && pip install goobook \
  && pip install mutt_ics \
  && rpm -e --nodeps --allmatches --noscripts \
	`rpm -qa | grep aaa_base` \
	`rpm -qa | grep acl | grep -v lib` \
	`rpm -qa | grep branding-openSUSE` \
	`rpm -qa | grep cpio` \
	`rpm -qa | grep cryptsetup` \
	`rpm -qa | grep dbus-1 | grep -v lib` \
	`rpm -qa | grep dracut` \
	`rpm -qa | grep fipscheck` \
	`rpm -qa | grep kbd` \
	`rpm -qa | grep kmod` \
	`rpm -qa | grep mapper` \
	`rpm -qa | grep ncurses-utils` \
	`rpm -qa | grep openSUSE-release` \
	`rpm -qa | grep pigz` \
	`rpm -qa | grep pkg-config` \
	`rpm -qa | grep qrencode` \
	`rpm -qa | grep sg3_utils` \
	`rpm -qa | grep systemd | grep -v lib` \
	curl \
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
