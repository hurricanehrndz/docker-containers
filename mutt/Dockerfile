# mutt-kz
FROM opensuse:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>

RUN zypper addrepo http://download.opensuse.org/repositories/home:hurricanehernandez/openSUSE_Tumbleweed/home:hurricanehernandez.repo \
 && zypper addrepo http://download.opensuse.org/repositories/server:mail/openSUSE_Tumbleweed/server:mail.repo \
 && zypper --gpg-auto-import-keys ref \
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
	pinentry \
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
	home_hurricanehernandez:mutt-kz \
 && zypper cc --all \
 && rm -rf /var/cache/zypp* \
 && rpm -e --nodeps --allmatches --noscripts \
	aaa_base \
	dbus-1 \
	dracut \
	kbd \
	kmod \
	ncurses-utils \
	pkg-config \
	sg3_utils \
	systemd \
	systemd-presets-branding-openSUSE \
	systemd-sysvinit \
	udev
#RUN update-ca-certificates \
# && git clone https://github.com/hurricanehrndz/vim /var/cache/.vim \
# && git clone https://github.com/altercation/vim-colors-solarized /var/cache/.vim/bundle/vim-colors-solarized \
# && git clone https://github.com/dbeniamine/vim-mail.git /var/cache/.vim/bundle/vim-mail
#
#ENV LC_LANG="en_CA.UTF-8" PINENTRY_BINARY="/usr/bin/pinentry-curses"
