# rdesktop

`Dockerfile` to create a [Docker](https://www.docker.com/) image of
[rdesktop](http://www.rdesktop.org/).

This container will attempt to mount the host's [X11](http://www.x.org) unix
domain socket in order to create its graphical window on the host's X11 server.

## Installation:
This container can be installed from either the [Docker
Hub](http://hub.docker.com/r/hurricane/rdesktop) or by cloning this project to your host and running
`make`. For most users installing from the hub will be sufficient.

This container is deployed with a wrapper script that makes running the docker
image very simple. Simply chose one of the installation methods below to get
started.

### Installing from [Docker Hub](http://hub.docker.com/r/hurricane/rdesktop):
```
docker run -it --rm \
    -v /usr/local/bin:/target \
    instl
```

### Installing from [github](http://github.com/hurricanehrndz/docker-containers):
```
git clone https://github.com/hurricanehrndz/docker-containers
cd rdesktop
make instl
```

## Usage
You can use this container however your imagination sees fit. The suggested
method though is via the wrapper script that comes bundled with this docker
image. You can start [rdesktop](http://rdesktop.org/), after installation,
by executing the following command:
```
rdesktop
```
You can of course also run this container manually by executing
the following:
```
XAUTH=/tmp/.docker.xauth
touch ${XAUTH}
xauth nlist :0 | sed -e 's/^..../ffff/' | xauth -f ${XAUTH} nmerge -
docker run -d -e DISPLAY \
    -e XAUTHORITY=${XAUTH} \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    hurricane/rdesktop
```

## Technical Information:
This container is developed on top of [openSUSE's
TumbleWeed](http://hub.docker.com/_/opensuse) base image. This
conscious decision was made to yield the smallest image possible.

The wrapper script, which gets installed by executing any of the suggested
installtion methods, makes running this container simple. The script will ensure
that the appropriate environment variables get passed onto the container.
Additionally, it ensures that the container gets automatically stopped once you
have exited rdesktop. These environment variables are as follows:
* `TZ`         - for timezone.
* `APP_UID`    - UID of the user executing the wrapper script
* `APP_GID`    - GID of the user executing the wrapper script
* `APP_USER`   - username of the user executing the wrapper script
* `DISPLAY`    - X11 display server name
* `XAUTHORITY` - authority file providing credentials to access X11 server

### Known Issues:
* None at the time of writing.
Feel free to report additional [issues](../../../issues/new).

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
* 2015-01-20 - initial release.

## License
Code released under the [MIT license](./LICENSE).
