FROM hurricane/jessie

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
	rdesktop \
	libgssapi-krb5-2 \
 && update-locale LANG=C.UTF-8 LC_MESSAGES=POSIX \
 && rm -rf /var/list/apt/lists/*
COPY scripts/ /var/cache/rdesktop/
COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

ENTRYPOINT ["/sbin/entrypoint.sh"]
