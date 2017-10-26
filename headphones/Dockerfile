FROM hurricane/base:x86_64
ARG ARCH
ENV APP_NAME="headphones" IMG_NAME="headphones" TAG_NAME="${ARCH}" S6_LOGGING="0" PYTHONIOENCODING="UTF-8" UMASK=002 EDGE=0

RUN zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive in --no-recommends \
	ca-certificates{-cacert,-mozilla} \
	curl \
	git-core \
	python \
	python-xml \
	tar \
	timezone \
 && mkdir -p /usr/lib/${APP_NAME} \
 && git clone --depth=1 https://github.com/rembo10/headphones.git /usr/lib/${APP_NAME} \
 && curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz -o /tmp/ffmpeg.tar.xz \
 && tar -C /bin --extract --file=/tmp/ffmpeg.tar.xz --wildcards "*/ffmpeg" --strip-components=1  \
 && tar -C /bin --extract --file=/tmp/ffmpeg.tar.xz --wildcards "*/ffprobe" --strip-components=1  \
 && rpm -e --nodeps --allmatches --noscripts \
	`rpm -qa | grep aaa_base` \
	`rpm -qa | grep acl | grep -v lib` \
	`rpm -qa | grep branding-openSUSE` \
	`rpm -qa | grep branding` \
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
 && zypper cc --all \
 && rm -rf /usr/share/{man,doc,info,gnome/help} \
 && rm -rf /var/cache/zypp* \
 && rm -rf /tmp/* \
 && rm -rf /var/log/*

COPY root /
VOLUME [ "/config" ]
EXPOSE 8181
ENTRYPOINT ["/init"]
