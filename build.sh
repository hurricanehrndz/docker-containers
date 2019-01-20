#!/usr/bin/env bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

docker_repo="hurricane"
#arches=(amd64)
arches=(amd64 arm64v8 arm32v7)
qemu_user_static_tmpdir="/var/tmp/qemu-static"
qemu_user_static_releases_url="https://github.com/multiarch/qemu-user-static/releases.atom"
qemu_user_static_target_url="https://github.com/multiarch/qemu-user-static/releases/download/__QEMU_VER__/x86_64_qemu-__QEMU_ARCH__-static.tar.gz"
s6_overlay_tmpdir="/var/tmp/s6-overlay"
s6_overlay_releases_url="https://github.com/just-containers/s6-overlay/releases.atom"
s6_overlay_target_url="https://github.com/just-containers/s6-overlay/releases/download/__S6_VER__/s6-overlay-__S6_ARCH__.tar.gz"

get_release_ver() {
  url="$1"
  curl -sL "$url" | awk '{
    if ($0 ~ "<entry>") { isRelease=1 }
    if (isRelease == 1 && $0 ~ "title" && done != 1) {
      ver=$0;
      gsub("(</|<)title>","",ver);
      gsub("[[:space:]]+","",ver);
      done=1
    }
  }
  END {printf "%s", ver;}'
}


new_build_dir() {
  container_name="$1"
  arch="$2"
  build_dir="/var/tmp/${docker_repo}_${container_name}_${arch}"
  mkdir -p "$build_dir"
  echo "$build_dir"
}

get_qemu_user_static() {
  target_arch="$1"
  build_dir="$2"

  url="$(echo "$qemu_user_static_target_url" | awk -v ver="$qemu_ver" '{gsub("__QEMU_VER__",ver); print $0}')"
  url="$(echo "$url" | awk -v arch="$target_arch" '{gsub("__QEMU_ARCH__",arch); print $0}')"
  arch_archive="${url##*/}"
  archive_full_path="${qemu_user_static_tmpdir}/${arch_archive}"

  if [[ ! -f "$archive_full_path" ]]; then
    echo "Downloading $url"
    curl -so "$archive_full_path" -L "$url"
  fi
  tar -xf "$archive_full_path" -C "$build_dir"
}

get_s6_overlay() {
  target_arch="$1"
  build_dir="$2"

  url="$(echo "$s6_overlay_target_url" | awk -v ver="$s6_ver" '{gsub("__S6_VER__",ver); print $0}')"
  url="$(echo "$url" | awk -v arch="$target_arch" '{gsub("__S6_ARCH__",arch); print $0}')"
  arch_archive="${url##*/}"
  archive_full_path="${s6_overlay_tmpdir}/${arch_archive}"

  if [[ ! -f "$archive_full_path" ]]; then
    echo "Downloading $url"
    curl -so "$archive_full_path" -L "$url"
  fi
  tar -xf "$archive_full_path" -C "${build_dir}/root"
}

prep_dockerfile() {
  build_dir="$1"
  docker_arch="$2"
  qemu_arch="$3"

  sed -i "s|__BASEIMAGE_ARCH__|${docker_arch}|g" "$build_dir/Dockerfile"
  sed -i "s|__QEMU_ARCH__|${qemu_arch}|g" "$build_dir/Dockerfile"
  if [ "${docker_arch}" == 'amd64' ]; then
    sed -i "/__CROSS_/d" "$build_dir/Dockerfile"
  else
    sed -i "s/__CROSS_//g"  "$build_dir/Dockerfile"
  fi
  echo "$build_dir"
}

sync_dirs() {
  src="$1"
  dst="$2"
  if [[ -z "$src" || -z "$dst" ]]; then
    exit 1
  fi
  rsync -a "$src/" "$dst/"
}

register_qemu_user_static() {
  if [[ (! -e /proc/sys/fs/binfmt_misc/qemu-arm || ! -e /proc/sys/fs/binfmt_misc/qemu-aarch64) ]]; then \
    docker run --rm --privileged multiarch/qemu-user-static:register > /dev/null
  fi
}

build_docker_image() {
  build_dir="$1"
  docker_image_tag="$2"

  docker build --no-cache=true --rm=true --tag="$docker_image_tag" "$build_dir"
  push_docker_image "$docker_image_tag"
}

push_docker_image() {
  docker_image_tag="$1"
  sync
  docker push "$docker_image_tag"
}

create_docker_manifest() {
  manifests="$1"
  container_name="$2"
  manifest_list="${docker_repo}/${container_name}:latest"
  docker manifest create $manifest_list $manifests
  sleep 30
  for manifest in $manifests; do
    if [[ $manifest =~ amd64 ]]; then
      continue
    fi
    if [[ $manifest =~ arm64v8 ]]; then
      manifest_opts="--arch arm64 --variant armv8"
    else
      manifest_opts="--arch arm --variant armv7"
    fi
    docker manifest annotate --os linux $manifest_opts $manifest_list $manifest
  done
  sync
  sleep 30
  docker manifest push --purge $manifest_list
}

clean() {
  container_name="$1"
  rm -rf "/var/tmp/${docker_repo}_*"
  docker image prune -f
  docker container prune -f
}

prep_for_builds() {
  docker image prune -f
  rm -rf "$qemu_user_static_tmpdir" "$s6_overlay_tmpdir"
  docker pull multiarch/qemu-user-static:register
  for arch in "${arches[@]}"; do
    docker pull "$arch/debian:stable"
  done
  mkdir -p "$qemu_user_static_tmpdir"
  mkdir -p "$s6_overlay_tmpdir"
}

build_docker_images() {
  container_name="$1"
  docker_image_tags=""
  for arch in "${arches[@]}"; do
    echo "Building $container_name for $arch"
    case $arch in
      amd64  ) qemu_arch="x86_64"  ; s6_arch="amd64"    ;;
      arm32v7) qemu_arch="arm"     ; s6_arch="armhf"    ;;
      arm64v8) qemu_arch="aarch64" ; s6_arch="aarch64"  ;;
    esac
    source_dir="${DIR}/${container_name}"
    build_dir="$(new_build_dir "$container_name" "$arch")"
    docker_image_tag="${docker_repo}/${container_name}:${arch}-latest"
    docker_image_tags="$docker_image_tags $docker_image_tag"
    sync_dirs "$source_dir" "$build_dir"
    get_qemu_user_static "$qemu_arch" "$build_dir"
    get_s6_overlay "$s6_arch" "$build_dir"
    prep_dockerfile "$build_dir" "$arch" "$qemu_arch"
    register_qemu_user_static
    build_docker_image "$build_dir" "$docker_image_tag"
  done
  create_docker_manifest "$docker_image_tags" "$container_name"
  clean "$container_name"
}


qemu_ver=$(get_release_ver "$qemu_user_static_releases_url")
s6_ver=$(get_release_ver "$s6_overlay_releases_url")

if [[ ! "${qemu_ver}" =~ v.* ]]; then
  exit 1
fi

prep_for_builds
container_names=("$@")
for container_name in "${container_names[@]}"; do
  echo "Building $container_name"
  build_docker_images "$container_name"
  sync
done

