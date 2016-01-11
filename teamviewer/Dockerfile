FROM opensuse:tumbleweed

RUN zypper ref \
 && zypper --non-interactive in fontconfig-32bit \
	libICE6-32bit \
	libSM6-32bit \
	libX11-6-32bit \
	libXau6-32bit \
	libXdamage1-32bit \
	libXext6-32bit \
	libXfixes3-32bit \
	libXinerama1-32bit \
	libXrandr2-32bit \
	libXrender1-32bit \
	libXtst6-32bit \
	libbz2-1-32bit \
	libexpat1-32bit \
	libfreetype6-32bit \
	libjpeg62-32bit \
	libpng12-0-32bit \
	libpng16-16-32bit \
	libuuid1-32bit \
	libxcb1-32bit \
	libasound2-32bit \
	libdbus-1-3-32bit \
	libgcc_s1-32bit \
	sudo \
	curl \
	tar \
	xz \
 && zypper cc --all \
 && rm -rf /var/cache/zypp* \
 && curl -sL http://download.teamviewer.com/download/teamviewer_i386.tar.xz -o /tmp/teamviewer_i386.tar.xz \
 && tar xf /tmp/teamviewer_i386.tar.xz -C /opt \
 && rm -rf /tmp/*

# s6-overlay
ADD s6-overlay-amd64.tar.gz /
COPY root /
# comment this out to debug
ENV S6_LOGGING="1"
ENTRYPOINT ["/init"]
