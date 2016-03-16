![Alt text](http://i.imgur.com/vuZVNSW.png "")

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
  - [Removal](#removal)
  - [Shell Access](#shell-access)
- [unRAID](#unraid)
  - [Installation](#unraid-installation)
  - [Automatic Upgrades](#unraid-automatic-upgrades)
- [Technical Information](#technical-information)
  - [Environment Variables](#environment-variables)
  - [Volumes](#volumes)
- [Manual Run and Installation](#manual-run-and-installation)
- [References](#references)
- [License](#license)
- [Donation](#donation)


# Introduction

[Quassel Core](http://quassel-irc.org/) is a daemon/headless distributed IRC client, that supports 24/7 connectivity.
The core maintains a persistent connection to IRC channels recording all the
action, while compatible clients connect/disconnect freely to the core without
fear of ever missing out in the conversation. This [Docker](https://www.docker.com) image of Quassel Core
has been configured with PostgreSQL for better performance and scalability.

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

### [Docker Hub](https://hub.docker.com/r/hurricane/quasselcore/):
It is recommended you install directly from the [Docker Hub](https://hub.docker.com/r/hurricane/quasselcore/).

The following command copies over a wrapper scrip that will create a container
named `quasselcore` when executed. The wrapper script will ensure that the
container gets setup with the appropriate environment variables and volumes
each time it is executed.

Start the installation by issuing the following command from within a terminal:
```
docker run -it --rm -v /usr/local/bin:/target \
    hurricane/quasselcore instl
```

### [GitHub](https://github.com/hurricane/docker-containers/quasselcore):
Installation from GitHub is recommended only for the purposes of
troubleshooting and development. To install Quassel Core from GitHub execute the
following:
```
git clone https://github.com/hurricane/docker-containers
cd docker-containers/quasselcore
make instl
```

### Initial Configuration:

Once the Quassel Core container has been pulled and the wrapper script installed you
can execute the wrapper script from a terminal:
```
quasselcore
```

The first time you run the Quassel Core container, you will need  setup a user
and password for a compatible client. You can add a user by executing the
following command and following the on screen prompts:
```
docker exec -ti quasselcore add-quassel-user
```

# Maintenance

## Upgrading:

If you have installed our systemd service file, you can update by
executing the following command:
```
sudo systemctl restart quasselcore.service
```

Additionally you can update by:
```
docker exec quasselcore update
```

Or by executing:
```
docker pull hurricane/quasselcore
docker stop quasselcore
quasselcore
```

## Automatic Upgrades:

In order to have the container periodically check and upgrade the subsonic
binary one needs to add  a [`crontab`](https://en.wikipedia.org/wiki/Cron)
entry. Like so:
```
echo "0 2 * * * docker exec quasselcore update" | sudo tee -a /var/spool/cron/crontabs/root
```

## Removal:

```bash
docker run -it --rm \
  --volume /usr/local/bin:/target \
  hurricane/quasselcore uninstl
```

## Shell Access

For debugging and maintenance purposes you may want access the containers
shell. If you are using Docker version `1.3.0` or higher you can access
a running containers shell by starting `bash` using `docker exec`:

```bash
docker exec -it quasselcore bash
```


# unRAID:

You can find the template for this container on GitHub. Located [here](https://github.com/hurricanehrndz/container-templates/tree/master/hurricane).

## unRAID Installation:

Please navigate to the Docker settings page on unRAID's Web-UI and under repositories add:
```
https://github.com/hurricanehrndz/container-templates/tree/master/hurricane
```
For more information on adding templates to unRAID please visit the [unRAID forums](https://lime-technology.com/forum/).

## unRAID Automatic Upgrades:

On unRAID, execute the following to have the container periodically update
itself. Additionally, add the same line of code to your `go` file to make the
change persistent.
```
echo "0 2 * * * docker exec quasselcore update" | sudo tee -a /var/spool/cron/crontabs/root
```


# Technical information:

By default the image has been created to run with UID and GID 1000. If using
the automatic install method from Docker, the container is set to run with the
UID and GID of of the user executing the `quasselcore` wrapper script.
Additionally, the wrapper script by default saves Quassel Core's config and the
PostgreSQL in a hidden sub folder in the executing user's home directory.

Here is a list of any and all applicable environment variables that
can be override by the end user.

## Environment Variables:

You may overwrite the default settings by passing the appropriate environment variable:
* APP_USER   - name of user to create within container for purposes of running mutt, UID, GID are more important.
* APP_UID    - UID assigned to APP_USER upon creation.
* APP_GID    - GID assigned to APP_USER upon creation.

Please read Docker documentation on [environment variables](https://docs.docker.com/engine/reference/run/#env-environment-variables) for more information.

## Volumes:

* `/home/$APP_USER/.quasselcore` - Quassel Core config and PostgreSQL database
  location


# Manual Run and Installation:

Of course you can always run the docker image manually. Please be aware that if
you want your data/configuration to persistent you need to provide a location
for the `/config` volume. For example,
```
docker run -d --net=host -v /*your_mail_dir*:/config \
                         -e TZ=America/Edmonton \
                         --name=quasselcore hurricane/quasselcore
```
All the information mention previously regarding user UID and GID still applies
when executing a docker run command.


# Known Issues:

- None at the time of writing.


# References:

- http://bugs.quassel-irc.org/projects/quassel-irc/wiki/PostgreSQL


# License:

Code released under the [MIT license](./LICENSE).


# Donation

[@hurricanehrndz](https://github.com/hurricanehrndz): [![PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=74S5RK533DD6C)
