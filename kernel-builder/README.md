# Kernel-Builder

`Dockerfile` to create a [Docker](https://www.docker.com/) image of
Kernel-Builder.

When running, the container will attempt to compile the linux kernel from
source for debian jessie. For more details on the process read on.

To start it uses debian's testing (stretch) config from kerenl 4.2 with optimizations
for docker as the starting config. It then executes menuconfig, so the user may
make any further changes deemed necessary. Then, the resultig config is copied
back to the root folder of the cloned repository. Finally, it begins to compile
the kernel and copie the resulting five debian packages back to the host.

## Installation

None required.

## Usage

```
git clone http://github.com/hurricanehrnz/kernel-builder
cd kernel-builder
make VERSION=4.3 kernel
```

This will produce five debian packages in the root folder of the cloned repository.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-newtt-feature`
5. Submit a pull request :D

## License
Code released under the (MIT license)[./LICENSE].

