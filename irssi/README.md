![Alt text](http://i.imgur.com/ir3vAxL.png "")

- [Introduction](#introduction)
  - [Contributing](#contributing)
  - [Issues](#issues)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Docker Hub](#docker-hub)
    - [GitHub](#github)
    - [Initial Configuration](#initial-configuration)
- [Maintenance](#maintenance)
  - [Upgrading](#upgrading)
  - [Removal](#removal)
  - [Shell Access](#shell-access)
- [Technical Information](#technical-information)
  - [Environment Variables](#environment-variables)
  - [Volumes](#volumes)
- [Manual Run and Installation](#manual-run-and-installation)
- [License](#license)
- [Donation](#donation)


# Introduction

Irssi is a text mode modular realtime chat client supporting IRC and SILC
protocols. This containerized version of Irssi is themed with a modified
version of [Huyz's solarized-universal theme](https://github.com/huyz/irssi-colors-solarized).

This subfolder contains all necessary files to build a [Docker](https://www.docker.com/) image for [ZNC](https://irssi.org).

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Issues

Before reporting your issue please try updating Docker to the latest version
and check if it resolves the issue. Refer to the Docker [installation guide](https://docs.docker.com/installation) for instructions.

SELinux users should try disabling SELinux using the command `setenforce 0` to see if it resolves the issue.

If the above recommendations do not help then [report your issue](../../issues/new) along with the following information:

- Output of the `docker version` and `docker info` commands
- The `docker run` command or `docker-compose.yml` used to start the image. Mask out the sensitive bits.
- Please state if you are using [Boot2Docker](http://www.boot2docker.io), [VirtualBox](https://www.virtualbox.org), etc.


# Getting started

## Installation:

### [Docker Hub](https://hub.docker.com/r/hurricane/irssi/):
It is recommended you install directly from the [Docker Hub](https://hub.docker.com/r/hurricane/irssi/).

The following command copies over a wrapper scrip that will create a container
named `znc` when executed. The wrapper script will ensure that the
container gets setup with the appropriate environment variables and volumes
each time it is executed.

Start the installation by issuing the following command from within a terminal:
```
docker run -it --rm -v /usr/local/bin:/target \
    hurricane/irssi instl
```

If the user you specified does not have a valid home directory you will
probably want to specify an alternate location to store the znc
configuration and back logs like so:
```
docker run -it --rm -v /usr/local/bin:/target \
    -e "APP_USER=username" \
    -e "APP_CONFIG=/var/lib/irssi" \
    hurricane/znc instl
```
Above, change the `username` to the name of the user you wish to run the daemon
as, and adjust `/var/lib/irssi` to wherever it is you wish to store Irssi's
configuration. Please verify that `$APP_USER` is the owner of `$APP_CONFIG`.

### [GitHub](https://github.com/hurricane/docker-containers/irssi):
Installation from GitHub is recommended only for the purposes of
troubleshooting and development. To install ZNC from GitHub execute the
following:
```
git clone https://github.com/hurricane/docker-containers
cd docker-containers/irssi
make instl
```

### Initial Configuration:

Once Irssi has been installed you can simply execute the binary from a terminal:
```
irssi
```

You can then add an irc server or a bouncer such as ZNC like so:
```
/network add freenode
/server add -net freenode -auto -ssl my.bouncer.net 6660 username/freenode:password
/save
/connect freenode
```

Once your connected you can set the `hilightwin` plugin to highlight your
nickname by issuing the following command:
```
/hilight hurricanehrndz
```

# Maintenance

## Upgrading:

You can update by executing the following:
```
docker pull hurricane/irssi
docker stop irssi
irssi
```
## Removal:

```bash
docker run -it --rm \
  --volume /usr/local/bin:/target \
  hurricane/irssi uninstl
```

## Shell Access

For debugging and maintenance purposes you may want access the containers
shell. If you are using Docker version `1.3.0` or higher you can access
a running containers shell by starting `bash` using `docker exec`:

```bash
docker exec -it irssi bash
```


# Technical information:

By default the image has been created to run with UID and GID 1000. If using
the automatic install method from Docker, the container is set to run with the
UID and GID of of the user executing the `irssi` wrapper script.  Additionally,
the wrapper script by default saves Irssi's configuration and settings in
a hidden sub folder in the executing user's home directory. Most default
settings can be adjusted by passing the appropriate environment variable. Here
is a list of any and all applicable environment variables that can be override
by the end user.

## Environment Variables:

You may overwrite the default settings by passing the appropriate environment variable:
* APP_USER   - name of user to create within container for purposes of running ZNC, UID, GID are more important.
* APP_UID    - UID assigned to APP_USER upon creation.
* APP_GID    - GID assigned to APP_USER upon creation.
* APP_CONFIG - the directory that should house Irssi's metadata and configuration.

Please read Docker documentation on [environment variables](https://docs.docker.com/engine/reference/run/#env-environment-variables) for more information.

## Volumes:

* `/home/${APP_USER}/.irssi`  - Folder to store Irssi's configuration and settings.


# Manual Run and Installation:

Of course you can always run docker image manually. Please be aware that if you
wish your data to remain persistent you need to provide a location for the
`/home/${APP_USER}/.irssi` volume. For example,
```
export APP_USER="username"
docker run -it --net=host -v /*your_config_location*:/home/${APP_USER}/.irssi \
                         -e TZ=America/Edmonton \
                         -e APP_USER=${APP_USER} \
                         -v /var/lib/irssi=/home/${APP_USER}/.irssi \
                         --name=irssi hurricane/irssi su ${APP_USER} -c irssi
```
All the information mention previously regarding user UID and GID still applies
when executing a docker run command.


# License

Code released under the [MIT license](./LICENSE).


# Donation

[@hurricanehrndz](https://github.com/hurricanehrndz): <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=74S5RK533DD6C"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" alt="[paypal]" /></a>
