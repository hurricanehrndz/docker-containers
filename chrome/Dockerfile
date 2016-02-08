FROM opensuse:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_CA.UTF-8" s6_overlay_version="1.17.1.1" APP_NAME="google-chrome" IMG_NAME="google-chrome" TAG_NAME="latest" S6_LOGGING="0"

RUN zypper --non-interactive addrepo -f http://download.nvidia.com/opensuse/leap/42.1 nvidia \
 && zypper --non-interactive addrepo -f  http://dl.google.com/linux/rpm/stable/x86_64 google-chrome \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in --no-recommends \
	adwaita-icon-theme \
	ca-certificates{,-cacert,-mozilla} \
	curl \
	dejavu-fonts \
	file \
	gconf2 \
	gdouros-symbola-fonts \
	glibc-locale \
	google-chrome-stable \
	hicolor-icon-theme \
	libappindicator3-1 \
	libcanberra-gtk2-0 \
	libcanberra-gtk2-module \
	libcurl4 \
	liberation2-fonts \
	libexif-devel \
	nvidia-glG04 \
	libpango-1_0-0 \
	libv4l1-0 \
	libXss1 \
	libXtst6 \
	Mesa \
	Mesa-libEGL1 \
	Mesa-libGL1 \
	Mesa-libglapi0 \
	mozilla-nspr \
	mozilla-nss \
	pulseaudio \
	tar \
	timezone \
	xz-utils \
	x11-video-nvidiaG04 \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
  && cd /usr/lib/locale \
  && ls | grep -ve "en_CA*\|en_US*" | xargs rm -rf \
  && cd /usr/share/locale \
  &&  find -name '*.mo' | grep -ve "en_US*" | xargs rm \
  && rpm -e --nodeps --allmatches --noscripts \
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
  && zypper cc --all \
  && rm -rf /usr/lib64/gconv/* \
  && rm -rf /usr/share/{man,doc,info,gnome/help} \
  && rm -rf /var/cache/zypp* \
  && rm -rf /tmp/* \
  && rm -rf /var/log/*

COPY root /
ENTRYPOINT ["/init"]
