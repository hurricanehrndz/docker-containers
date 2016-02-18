![Alt text](http://www.activeobjects.no/subsonic/forum/templates/subSilver/images/logo_phpBB.gif "")

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
  - [Automatic Upgrades](#automatic-upgrades)
  - [Uninstallation](#uninstallation)
  - [Shell Access](#shell-access)
- [License](#license)

# Introduction

Subsonic is an open source, web-based media server.

Because Subsonic was written in Java, it may be run on any operating system
with Java support.  Subsonic supports streaming to multiple clients
simultaneously, and supports any streamable media (including MP3, AAC, and
Ogg).  Subsonic also supports on-the-fly media conversion (through the use of
plugins) of most popular media formats, including WMA, FLAC, and more.

This subfolder contains all necessary files to build a [Docker](https://www.docker.com/) image for [Subsonic](www.subsonic.org).

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

## Prerequisites

* ensure the user running the installation command can run docker

## Installation:

### [Docker Hub](https://hub.docker.com/r/hurricane/subsonic/):
It is recommended you install directly from the [Docker Hub](https://hub.docker.com/r/hurricane/subsonic/).
Before starting the install procedure please verify the following prerequisites
are fulfilled:

Start the installation by issuing the following command from within a terminal:
```
docker run -it --rm -v /usr/local/bin:/target \
    hurricane/subsonic instl
```

Optionally, you can also install a systemd service file. Before installing the
systemd service file, you might want specify which user you wish the daemon to
run as, specifically if it differs from the user running the installation. You
can do this by reinstalling subsonic with the following command:
```
docker run -it --rm -v /usr/local/bin:/target -e "APP_USER=username" \
    hurricane/subsonic instl
```

If the user you specified does not have a valid home directory you will
probably want to specify an alternate location to store the subsonic
configuration and database like so:
```
docker run -it --rm -v /usr/local/bin:/target \
    -e "APP_USER=username" \
    -e "APP_CONFIG=/var/lib/subsonic" \
    hurricane/subsonic instl
```
Above, change the `username` to the name of the user you wish to run the daemon
as, and adjust `/var/lib/subsonic` to wherever it is you wish to store your
subsonic database and information. Please verify that `$APP_USER` is the owner
of `$APP_CONFIG`.

Afterward, proceed with the service file installation:
```
docker run -it --rm -v /etc/systemd/system:/target \
   hurricane/subsonic instl service
```

If you installed the systemd service file, you can enable Subsonic to
automatically start when the system boots by executing the following command:
```
sudo systemctl enable subsonic.service
```
### [GitHub](https://github.com/hurricane/docker-containers/subsonic):
Installation from GitHub is recommended only for the purposes of
troubleshooting and development. To install Subsonic from GitHub execute the
following:
```
git clone https://github.com/hurricane/docker-containers
cd docker-containers/subsonic
make instl
```

Additionally, you can install the systemd service file after executing the
above by issuing the following:
```
make service
```
### Initial Configuration:

Once Subsonic has been installed you can simply execute the binary from a terminal:
```
subsonic
```

The first time you run the Subsonic container it will prompt you for the
locations of `MUSIC`, `PODCASTS`, and `PLAYLISTS`. Enter one response per
query.  This will ensure that the container gets access to the host's file
system from within the containerized environment.

# Maintenance

## Upgrading:
If you have installed our systemd service file, you can update by
executing the following command:
```
sudo systemctl restart subsonic.service
```

Additionally you can update by:
```
docker exec subsonic update
```

Or by executing:
```
docker pull hurricane/subsonic
docker stop subsonic
subsonic
```
## Automatic Upgrades:
In order to have the container periodically check and upgrade the subsonic
binary one needs to add  a [`crontab`](https://en.wikipedia.org/wiki/Cron)
entry. Like so:
```
echo "0 2 * * * docker exec subsonic update" | sudo tee -a /var/spool/cron/crontabs/root
```
## Uninstallation

```bash
docker run -it --rm \
  --volume /usr/local/bin:/target \
  hurricane/subsonic uninstl
```

## Shell Access

For debugging and maintenance purposes you may want access the containers
shell. If you are using Docker version `1.3.0` or higher you can access
a running containers shell by starting `bash` using `docker exec`:

```bash
docker exec -it subsonic bash
```

## unRAID:
You can find the template for this container on GitHub. Located [here](https://github.com/hurricanehrndz/container-templates/tree/master/hurricane).

### Automatic Updates:
On unRAID you can execute and add the line of code that follows to your `go`
file to have the container automatically update.
```
echo "0 2 * * * docker exec subsonic update" | sudo tee -a /var/spool/cron/crontabs/root
```

### Installtion:
Please navigate to the Docker settings page on unRAID's Web-UI and under repositories add:
```
https://github.com/hurricanehrndz/container-templates/tree/master/hurricane
```
For more information on adding templates to unRAID please visit the [unRAID forums](https://lime-technology.com/forum/).

## Technical information:
This image and installation process setups Subsonic to run with the permissions
of the user executing `subsonic`. So, Subsonic's data is set to save within the
user's home directory under the subdirectory named `.subsonic`.

You may overwrite the default settings by passing the appropriate environment variable:
* APP_USER - name of user to create within container for purposes of running subsonic, UID, GID are more important.
* APP_UID - UID assigned to APP_USER upon creation.
* APP_GID - GID assigned to APP_USER upon creation.
* APP_CONFIG - the directory that should house Subsonic  metadata and configuration.

Please read Docker documentation on [environment variables](https://docs.docker.com/engine/reference/run/#env-environment-variables) for more information.

## Manual Run and Installtion:
Of course you can always run docker image manually. Please be aware that if you
wish your data to remain persistent you need to provide a location for the
`/config` volume. For example,
```
docker run -d -v /home/user/.subsonic:/subsonic hurricane/subsonic
```
All the information mention previously regarding user UID and GID still applies
when executing a docker run command.

## License
Code released under the [MIT license](./LICENSE).
