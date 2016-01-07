#!/bin/bash

sed -i -e 's:path=/home:path=/home/${USER}/.mail' ~/.notmuch-config
