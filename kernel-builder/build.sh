#!/bin/bash

mkdir -p /root
cd /root

if [ ! -f linux-${VERSION}.tar.xz ]; then
  if [[ "$VERSION" == *-rc* ]]; then
    wget https://www.kernel.org/pub/linux/kernel/v${VERSION%%.*}.x/testing/linux-${VERSION}.tar.xz
  else
    wget https://www.kernel.org/pub/linux/kernel/v${VERSION%%.*}.x/linux-${VERSION}.tar.xz
  fi
fi

cd /usr/src
test -d linux-${VERSION} || tar xJvfp /root/linux-${VERSION}.tar.xz

cd /usr/src/linux-${VERSION}
test -f /data/config && cp /data/config .config
test -f .config || cp /root/default-config .config

tty > /dev/null && make menuconfig


MAJOR_VERSION=${VERSION:0:1}
V=( ${VERSION//./ } )
MAJOR_MINOR_VERSION="${V[0]}.${V[1]}"
if [[ "$VERSION" == *-rc* ]] && [ "${VERSION:0:1}" == "4" ]; then
 MAJOR_MINOR_VERSION="4.x-rcN"
fi

# get the aufs standalone source
aufsdir=/usr/src/aufs4-standalone
if [[ -d $aufsdir ]]; then
  rm -rf $aufsdir
fi
git clone -b aufs${MAJOR_MINOR_VERSION} --single-branch --depth 1 https://github.com/sfjro/aufs4-standalone.git $aufsdir
cd $aufsdir

cd /usr/src/linux-${VERSION}

# apply the aufs patches
git apply $aufsdir/aufs4-kbuild.patch
git apply $aufsdir/aufs4-base.patch
git apply $aufsdir/aufs4-mmap.patch
cp -r $aufsdir/{Documentation,fs} .
cp $aufsdir/include/uapi/linux/aufs_type.h include/uapi/linux/

# remove aufs source
rm -rf $aufsdir

echo "CONFIG_AUFS_FS=y" >> .config

nice -19 make -j$JOBS KDEB_PKGVERSION=$PKGVERSION INSTALL_MOD_STRIP=1 deb-pkg
cp .config /data/config
cp /usr/src/*.deb /data/
bash
