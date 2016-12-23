FROM scratch
MAINTAINER Carlos Hernandez <carlos@techbyte.ca>
ARG ARCH=amd64
ENV LANG="en_US.UTF-8"

ADD rootfs.tar.xz       /
ADD overlay-common      /
ADD overlay-${ARCH}     /
