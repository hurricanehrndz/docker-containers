FROM scratch
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ADD openSUSE-Tumbleweed.tar.xz /
RUN zypper -n ar -f http://download.opensuse.org/tumbleweed/repo/oss repo-oss && \
    zypper -n ar -f http://download.opensuse.org/tumbleweed/repo/non-oss repo-non-oss && \
    zypper -n ar -f http://download.opensuse.org/update/tumbleweed/ repo-update && \
    zypper -n ar -f -d http://download.opensuse.org/tumbleweed/repo/debug repo-debug
