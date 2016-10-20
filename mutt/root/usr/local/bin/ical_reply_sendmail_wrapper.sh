#!/bin/bash
HOME=/home/$APP_USER

if [[ -z "$1" ]]; then
  exit 0
else
  active_account="$1"
  shift
fi

# get $sendmail from mutt
SENDMAIL=$(cat $HOME/.mutt/$active_account | sed -n "s/^set\ssendmail\s=\s\(.*\)/\1/p" | sed -s 's/"//g')

# fix header for ical reply and pipe to sendmail
sed '/^Content-Type: text\/calendar;/s/$/; METHOD="REPLY"/'|
sed '/^Content-Disposition: attachment/s/attachment/inline/g'|
$SENDMAIL "$@"

# this may also be necessary:
#sed '/^Content-Type: multipart\/mixed/s/mixed/alternative/g'|
