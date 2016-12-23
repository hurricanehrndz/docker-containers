FROM scratch
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ARG ARCH=amd64
ENV LANG="C.utf8"

ADD rootfs.tar.xz       /
ADD overlay-common      /
ADD overlay-${ARCH}     /
