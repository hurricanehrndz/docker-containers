FROM opensuse:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_US.UTF-8" s6_overlay_version="1.17.1.2" APP_NAME="mutt" IMG_NAME="mutt" TAG_NAME="latest" S6_LOGGING="1" TERM=xterm-256color

RUN zypper --non-interactive addrepo http://download.opensuse.org/repositories/home:hurricanehernandez/openSUSE_Tumbleweed/home:hurricanehernandez.repo \
 && zypper --non-interactive addrepo http://download.opensuse.org/repositories/home:AndnoVember:test/openSUSE_Factory/home:AndnoVember:test.repo \
 && zypper --non-interactive addrepo http://download.opensuse.org/repositories/server:mail/openSUSE_Tumbleweed/server:mail.repo \
 && zypper --non-interactive addrepo -f -c http://download.opensuse.org/repositories/home:/namtrac:/subpixel/openSUSE_Factory/ repo-namtrac \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
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
	libcrypto37 \
	libgpgme11 \
	libgtk-2_0-0 \
	libidn11 \
	libnotmuch4 \
	libsasl2-3 \
	libslang2 \
	libssl38 \
	libtokyocabinet9 \
	mirage \
	msmtp \
	notmuch \
	python \
	python-pyinotify \
	python-base \
	python-pip \
	python-PyYAML \
	repo-namtrac:freetype2 \
	tar \
	timezone \
	vim-data \
	vim-enhanced \
	w3m \
	zathura \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && curl -skL http://sourceforge.net/projects/davmail/files/davmail/4.7.1/davmail-linux-x86_64-4.7.1-2416.tgz -o /tmp/davmail.tgz \
  && mkdir -p /usr/lib/davmail \
  && tar xf /tmp/davmail.tgz --strip-components=1  -C /usr/lib/davmail/ \
  && cd /usr/lib/locale \
  && ls | grep -ve "en_CA*\|en_US*" | xargs rm -rf \
  && cd /usr/share/locale \
  &&  find -name '*.mo' | grep -ve "en_US*" | xargs rm \
  && git clone --depth 1 https://github.com/hurricanehrndz/vim /var/cache/.vim \
  && git clone --depth 1 https://github.com/dbeniamine/vim-mail /var/cache/.vim/bundle/vim-mail \
  && git clone --depth 1 https://github.com/altercation/vim-colors-solarized /var/cache/.vim/bundle/vim-colors-solarized \
  && pip install --upgrade pip \
  && pip install goobook \
  && pip install mutt_ics \
  && rpm -e --nodeps --allmatches --noscripts \
	`rpm -qa | grep cpio` \
	`rpm -qa | grep cryptsetup` \
	`rpm -qa | grep kbd` \
	`rpm -qa | grep kmod` \
	`rpm -qa | grep mapper` \
	`rpm -qa | grep openSUSE-release` \
	`rpm -qa | grep perl` \
	`rpm -qa | grep pigz` \
	`rpm -qa | grep pinentry` \
	`rpm -qa | grep qrencode` \
	aaa_base \
	curl \
	dracut \
	git-core \
	kmod \
	ncurses-utils \
	pkg-config \
	sg3_utils \
	systemd \
	systemd-presets-branding-openSUSE \
	systemd-sysvinit \
	tar \
  && localedef -i en_US -f UTF-8 en_US.UTF-8 \
  && zypper cc --all \
  && rm -rf /tmp/* \
  && rm -rf /usr/share/{man,doc,info,gnome/help} \
  && rm -rf /var/cache/zypp* \
  && rm -rf /var/log/*

COPY root /
ENTRYPOINT ["/init"]
