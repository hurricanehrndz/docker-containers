![Alt text](http://lh4.googleusercontent.com/-q47dEtTYAvg/UzLiFOIRj5I/AAAAAAAAFbg/NlsdH2FAm50/s800/mutt-128x128.png "")

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
- [Technical Information](#technical-information)
  - [Environment Variables](#environment-variables)
  - [Volumes](#volumes)
- [Manual Run and Installation](#manual-run-and-installation)
- [References](#references)
- [License](#license)
- [Donation](#donation)


# Introduction


![Alt text](http://i.imgur.com/yK3B9lt.png "")

[Mutt](www.mutt.org) is a small but very powerful text-based mail client for Unix operating
systems. This [Docker](https://www.docker.com) image has been designed and
bundled with added features for ease of use and functionality. These extra
features include but are not limited to:

- automatic configuration of maildir services (isync)
- out of box support for GMail and exchange
- address book support via goobook
- mutt sidebar
- GMail style keyboard shortcuts
- multiple email account support
- fast global search (notmuch via Mutt-kz)
- tag support (notmuch via Mutt-kz)
- ics support via mutt-ics
- two way sync of maildir folders (GMail tags) and notmuch tags
- solarized theme


This container and its functionality is provided without warranties or
guarantees. Please ensure you backup your email accounts before trying this
container out. Additionally, ensure any existing exchange folders or GMail
labels have been named without any periods or spaces.

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

## Prerequisites:

* GPG key per account.
* Global GPG key exported as environment variable named GPGKEY
* gnupg2
* email account info provided in yaml config file acsii encrypted with global
  GPG key.

## Preparation:

Setup a YAML file named `~/muttsecrets` with your email account or accounts
info like in the examples that follow.

Below is an example of a YAML configuration file for a GMail account.
```
- 01_domain:
    type: gmail
    name: John Smith
    email: jsmith@gmail.com
    user: jsmith@gmail.com
    pass: password
    smtp: smtp.gmail.com
    smtp_port: 465
    imap: imap.gmail.com
    gpg: '0xFFFFFFFF'
    signature: |
        Best Regards,
        John Smith
```

Here is an example of a YAML configuration file for an exchange account.
```
- 01_domain:
    type: exchange
    name: John Smith
    email: jsmith@domain.com
    user: jsmith
    pass: password
    smtp: 127.0.0.1
    smtp_port: 465
    imap: 127.0.0.1
    imap_port: 993
    gpg: '0xFFFFFFFF'
    signature: |
        Best Regards,
        John Smith
    davmail: |
        davmail.server=true
        davmail.enableEws=auto
        davmail.url=https://mail.domain.com/owa/
        davmail.imapPort=993
        davmail.smtpPort=465
        davmail.defaultDomain=domain
        davmail.allowRemote=false
        davmail.bindAddress=127.0.0.1

```

Finally encrypt the YAML file with the global GPG key you setup earlier. i.e.
```
gpg2 -o ~/.muttsecrets -r $GPGKEY ~/muttsecrets
```

## Installation:

### [Docker Hub](https://hub.docker.com/r/hurricane/mutt/):
It is recommended you install directly from the [Docker Hub](https://hub.docker.com/r/hurricane/mutt/).
Before starting the install procedure please verify that any and all
prerequisites are fulfilled:

The following command copies over a wrapper scrip that will create a container
named `mutt` when executed. The wrapper script will ensure that the
container gets setup with the appropriate environment variables and volumes
each time it is executed.

Start the installation by issuing the following command from within a terminal:
```
docker run -it --rm -v /usr/local/bin:/target \
    hurricane/mutt instl
```

### [GitHub](https://github.com/hurricane/docker-containers/mutt):
Installation from GitHub is recommended only for the purposes of
troubleshooting and development. To install Subsonic from GitHub execute the
following:
```
git clone https://github.com/hurricane/docker-containers
cd docker-containers/mutt
make instl
```

### Initial Configuration:

Once the mutt container has been pulled and the wrapper script installed you
can execute the wrapper script from a terminal:
```
mutt
```

The first time you run the mutt container, it will do an initial sync and
tagging of emails based on maildir folders.


# Maintenance

## Upgrading:

```
docker pull hurricane/mutt
docker stop mutt
mutt
```

## Removal:

```bash
docker run -it --rm \
  --volume /usr/local/bin:/target \
  hurricane/mutt uninstl
```

## Shell Access

For debugging and maintenance purposes you may want access the containers
shell. If you are using Docker version `1.3.0` or higher you can access
a running containers shell by starting `bash` using `docker exec`:

```bash
docker exec -it mutt bash
```

# Technical information:

By default the image has been created to run with UID and GID 1000. If using
the automatic install method from Docker, the container is set to run with the
UID and GID of of the user executing the `mutt` wrapper script. Additionally,
the wrapper script by default saves mutt's maildir structure in a hidden sub
folder in the executing user's home directory.

Here is a list of any and all applicable environment variables that
can be override by the end user.

## Environment Variables:

You may overwrite the default settings by passing the appropriate environment variable:
* APP_USER   - name of user to create within container for purposes of running mutt, UID, GID are more important.
* APP_UID    - UID assigned to APP_USER upon creation.
* APP_GID    - GID assigned to APP_USER upon creation.

Please read Docker documentation on [environment variables](https://docs.docker.com/engine/reference/run/#env-environment-variables) for more information.

## Volumes:

* `/home/$APP_USER/.mail` - root maildir directory
* `/home/$APP_USER/mutt/cache` - mutt cache directory


# Manual Run and Installation:

Of course you can always run docker image manually. Please be aware that if you
wish your data to remain persistent you need to provide a location for the
`/config` volume. For example,
```
docker run -d --net=host -v /*your_mail_dir*:/home/$USER/.mail \
                         -e TZ=America/Edmonton \
                         --name=mutt hurricane/mutt
```
All the information mention previously regarding user UID and GID still applies
when executing a docker run command.

# Known Issues:

- mbsync passwords stored in plain text within container
- msmtp password stored in plain text within cotainer
- desktop notifications requried.

# References:

- https://github.com/altercation/es-bin/blob/master/maildir-notmuch-sync
- https://github.com/altercation/es-etc/tree/master/mail
- http://stevelosh.com/blog/2012/10/the-homely-mutt/
- https://wiki.archlinux.org/index.php/Isync
- https://github.com/altercation/mutt-colors-solarized
- https://wiki.archlinux.org/index.php/msmtp


# License:

Code released under the [MIT license](./LICENSE).


# Donation

[@hurricanehrndz](https://github.com/hurricanehrndz): [![PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=74S5RK533DD6C)
