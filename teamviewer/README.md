# Teamviewer

`Dockerfile` to create a [Docker](https://www.docker.com/) image of
[teamviewer](http://teamviewer.com).

This container will attempt to mount the host's [X11](http://www.x.org) unix
domain socket in order to create its graphical window on the host's X11 server.

## Installation:
This container can be installed from either the [Docker
Hub](http://hub.docker.com/hurricane/teamviewer) or by cloning this project to your host and running
`make`. For most users installing from the hub will be sufficient.

This container is deployed with a wrapper script that makes running the docker
image very simple. Simply chose one of the installation methods below to get
started.

### Installing from [Docker Hub](http://hub.docker.com/hurricane/teamviewer):
```
docker run -it --rm \
    -v /usr/local/bin:/target \
    instl
```

### Installing from [github](http://github.com/hurricanehrndz/docker-containers):
```
git clone https://github.com/hurricanehrndz/docker-containers
cd teamviewer
make instl
```

## Usage
You can use this container however your imagination sees fit. The suggested
method though is via the wrapper script that comes bundled with this docker
image. You can start [TeamViewer](http://teamviewer.com), after installation,
by executing the following command:
```
teamviewer
```
You can of course also run this container manually by executing a command like in
the example below:
```
docker run -d -e DISPLAY \
    -e XAUTHORITY=${XAUTHORITY} \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    hurricane/teamviewer
```

## Technical Information:
This container is developed on top of [openSUSE's
TumbleWeed](http://hub.docker.com/_/opensuse) base image. This
conscious decision was made to yield the smallest image possible.

The wrapper script, which gets installed by executing any of the suggested
installtion methods, makes running this container simple. The script will ensure
that the appropriate environment variables get passed onto the container.
Additionally, it ensures that the container gets automatically stopped once you
have exited TeamViewer. These environment variables are as follows:
* `TZ`         - for timezone.
* `USER_UID`   - UID of the user executing the wrapper script
* `USER_GID`   - GID of the user executing the wrapper script
* `APP_USER`   - username of the user executing the wrapper script
* `DISPLAY`    - X11 display server name
* `XAUTHORITY` - authority file providing credentials to access X11 server

### Known Issues:
* system tray icon gets rendered on desktop as a large blue window  using  [i3 wm](https://i3wm.org).
  It is recommended to add the following three lines to you i3 config in order to
  stop the tray icon from being rendered at all.
```
for_window [instance="TeamViewer.exe"] floating enable
for_window [class="TeamViewer"] floating enable
for_window [instance="Qt-subapplication" title="TeamViewer"] move scratchpad
```
Feel free to report additional [issues](../../../issues/new).

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
* 2015-12-18 - TeamViewer 11, initial release.

## License
Code released under the [MIT license](./LICENSE).
