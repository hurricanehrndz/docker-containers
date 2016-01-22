FROM opensuse:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_CA.UTF-8" s6_overlay_version="1.17.1.1" APP_NAME="mutt" IMG_NAME="mutt" TAG_NAME="latest" S6_LOGGING="1"

RUN zypper addrepo http://download.opensuse.org/repositories/home:hurricanehernandez/openSUSE_Tumbleweed/home:hurricanehernandez.repo \
 && zypper addrepo http://download.opensuse.org/repositories/server:mail/openSUSE_Tumbleweed/server:mail.repo \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in --no-recommends ca-certificates{,-cacert,-mozilla} \
	git-core \
	w3m \
	w3m-inline-image \
	vim \
	python \
	python-base \
	python-PyYAML \
	isync \
	msmtp \
	glibc-locale \
	libcrypto36 \
	libgpgme11 \
	krb5-mini \
	libidn11 \
	libnotmuch4 \
	libsasl2-3 \
	libslang2 \
	libssl37 \
	libtokyocabinet9 \
	curl \
	notmuch \
	tar \
	home_hurricanehernandez:mutt-kz \
	timezone \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && cd /usr/lib/locale \
  && ls | grep -ve "en_CA*\|en_US*" | xargs rm -rf \
  && cd /usr/share/locale \
  &&  find -name '*.mo' | grep -ve "en_US*" | xargs rm \
  && git clone --depth 1 https://github.com/hurricanehrndz/vim /var/cache/.vim \
  && git clone --depth 1 https://github.com/dbeniamine/vim-mail /var/cache/.vim/bundle/vim-mail \
  && git clone --depth 1 https://github.com/altercation/vim-colors-solarized /var/cache/.vim/bundle/vim-colors-solarized \
  && rpm -e --nodeps --allmatches --noscripts \
	aaa_base \
	dbus-1 \
	dracut \
	kmod \
	ncurses-utils \
	pkg-config \
	sg3_utils \
	systemd \
	systemd-presets-branding-openSUSE \
	systemd-sysvinit \
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
	git-core \
  && zypper cc --all \
  && rm -rf /usr/share/{man,doc,info,gnome/help} \
  && rm -rf /var/cache/zypp* \
  && rm -rf /tmp/* \
  && rm -rf /var/log/*

COPY root /
ENTRYPOINT ["/init"]
