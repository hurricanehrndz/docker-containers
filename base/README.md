# Base
![Alt text](https://en.opensuse.org/images/thumb/e/e6/Tumbleweed-black-green.png/500px-Tumbleweed-black-green.png "")
- [Introduction](#introduction)
  - [Contributing](#contributing)
  - [Issues](#issues)
- [License](#license)
- [Donation](#donation)


# Introduction

Tumbleweed base image with native compiled s6-overlay pre-installed.

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


# License

Code released under the [MIT license](./LICENSE).


# Donation
[@hurricanehrndz](https://github.com/hurricanehrndz): [![PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=74S5RK533DD6C)
