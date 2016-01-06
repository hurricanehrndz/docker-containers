FROM hurricane/debianbase:stretch
MAINTAINER hurricaenhrndz <carlos@techbyte.ca>

RUN apt-get update \
 && apt-get install -y \
	ca-certificates \
	git \
	wget \
	kernel-package \
	make \
	libncurses5-dev \
	libssl-dev \
	libfile-fcntllock-perl \
 && rm -rf /var/lib/apt/lists/*

ENV HOME /root
WORKDIR $HOME

ENV JOBS 4

COPY build.sh /root/build.sh
COPY default-config /root/

CMD [ "/root/build.sh" ]
