FROM opensuse/amd64:tumbleweed
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ENV LANG="en_US.UTF-8" s6_overlay_version="1.18.1.5" APP_NAME="teamviewer" IMG_NAME="teamviewer" TAG_NAME="latest" S6_LOGGING="1"

RUN zypper --non-interactive addrepo -f -c http://download.opensuse.org/repositories/home:/namtrac:/subpixel/openSUSE_Factory/ repo-namtrac \
 && zypper --gpg-auto-import-keys ref \
 && zypper --non-interactive up \
 && zypper --non-interactive in --no-recommends \
	curl \
	fontconfig \
	fontconfig-32bit \
	glibc-locale \
	libasound2-32bit \
	libbz2-1-32bit \
	libdbus-1-3-32bit \
	libexpat1-32bit \
	libfreetype6-32bit \
	libgcc_s1-32bit \
	libICE6-32bit \
	libjpeg62-32bit \
	libpng12-0-32bit \
	libpng16-16-32bit \
	libSM6-32bit \
	libuuid1-32bit \
	libX11-6-32bit \
	libXau6-32bit \
	libxcb1-32bit \
	libXdamage1-32bit \
	libXext6-32bit \
	libXfixes3-32bit \
	libXinerama1-32bit \
	libXrandr2-32bit \
	libXrender1-32bit \
	libXtst6-32bit \
	repo-namtrac:freetype2 \
	tar \
	timezone \
	xz \
  && curl -sL http://download.teamviewer.com/download/teamviewer_i386.tar.xz -o /tmp/teamviewer_i386.tar.xz \
  && tar xf /tmp/teamviewer_i386.tar.xz -C /opt \
  && curl -skL https://github.com/just-containers/s6-overlay/releases/download/v${s6_overlay_version}/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay-amd64.tar.gz \
  && tar xf /tmp/s6-overlay-amd64.tar.gz -C / \
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
