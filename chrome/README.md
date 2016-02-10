# hurricane/google-chrome:latest

- [Introduction](#introduction)
  - [Contributing](#contributing)
  - [Issues](#issues)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [How it works](#how-it-works)
- [Maintenance](#maintenance)
  - [Upgrading](#upgrading)
  - [Uninstallation](#uninstallation)
  - [Shell Access](#shell-access)
- [References](#references)
- [License](#license)

# Introduction

`Dockerfile` to create a [Docker](https://www.docker.com/) container image consisting of google-chrome.

The image uses [X11](http://www.x.org) and
[Pulseaudio](http://www.freedesktop.org/wiki/Software/PulseAudio/) unix domain
sockets on the host to enable audio/video support in the web browsers. These
components are available out of the box on pretty much any modern linux
distribution.

![browser](https://cloud.githubusercontent.com/assets/410147/4377777/2ccda3d2-4352-11e4-9314-122e4f58a30c.gif)

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Issues

Before reporting your issue please try updating Docker to the latest version
and check if it resolves the issue. Refer to the Docker [installation
guide](https://docs.docker.com/installation) for instructions.

SELinux users should try disabling SELinux using the command `setenforce 0` to see if it resolves the issue.

If the above recommendations do not help then [report your issue](../../issues/new) along with the following information:

- Output of the `docker version` and `docker info` commands
- The `docker run` command or `docker-compose.yml` used to start the image. Mask out the sensitive bits.
- Please state if you are using [Boot2Docker](http://www.boot2docker.io), [VirtualBox](https://www.virtualbox.org), etc.

# Getting started

## Prerequisites
The image has been specifically designed to work with  pulseaudio version 7.x.
Pulseaudio 7.x by default comes with srbchannel on, this feature unfortunately
does not work within jail, chroot, and docker type of environments. As a result
users will need to edit "/etc/pulse/default.pa" in order to disabled it. It can
be disabled by passing the option `srbchannel=no` to the
module-native-protocol-unix in /etc/pulse/default.pa.

For more information please see the following [bug report](https://bugs.freedesktop.org/show_bug.cgi?id=92141)

Furthermore, the image has been built to take adavatange of hardware
acceleration with Nvidia GPUs. Please visit [chrome://gpu](chrome://gpu) to
verify that chrome is using hardware acceleration. You might need to enable
`#ignore-gpu-blacklist` flag with chrome for full acceleration. This can be
done at [chrome://flags](chrome://flags)

## Installation

This image is available as a [trusted build](//hub.docker.com/r/hurricane/google-chrome) on the [Docker hub](//hub.docker.com) and is the recommended method of installation.

```bash
docker pull hurricane/google-chrome:latest
```

Alternatively you can build the image yourself.

```bash
git clone https://github.com/hurricanehrndz/docker-containers.git
cd docker-containers/chrome
docker build --tag $USER/google-chrome .
```

With the image locally available, install the wrapper script using:

```bash
docker run -it --rm \
  --volume /usr/local/bin:/target \
  hurricane/google-chrome:latest instl
```
or

```bash
docker run -it --rm \
  --volume /usr/local/bin:/target \
  --env APP_REPO=$USER \
  $USER/google-chrome:latest instl
```
This will install a wrapper script to launch `google-chrome`.  This wrapper
script will ensure your chrome settings remain persistent by saving chrome's
application data in your home directory within a hidden subdirectory named
`.google-chrome`

## How it works

The wrapper script volume mount the X11 and pulseaudio sockets in the launcher
container. The X11 socket allows for the user interface to be display on the
host, while the pulseaudio socket allows for the audio output to be rendered on
the host.

# Maintenance

## Upgrading

To upgrade to newer releases:

  1. Download the updated Docker image:

  ```bash
  docker pull hurricane/google-chrome:latest
  ```

  2. Run `install` to make sure the host scripts are updated.

  ```bash
  docker run -it --rm \
    --volume /usr/local/bin:/target \
    hurricane/chrome:latest instl
  ```

## Uninstallation

```bash
docker run -it --rm \
  --volume /usr/local/bin:/target \
  hurricane/google-chrome:latest uninstl
```

## Shell Access

For debugging and maintenance purposes you may want access the containers
shell. If you are using Docker version `1.3.0` or higher you can access
a running containers shell by starting `bash` using `docker exec`:

```bash
docker exec -it google-chrome bash
```

# References

- http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/
- http://github.com/sameersbn/docker-browser-box
- https://bugs.freedesktop.org/show_bug.cgi?id=92141
- https://github.com/netblue30/firejail/issues/69

## License
Code released under the [MIT license](./LICENSE).
