#!/bin/bash

default_tags=("INBOX" "flagged" "important" "sent" "drafts" "archive" "trash" "spam")
result=""

pad_string() {
	pad=$(printf '%0.1s' "="{1..60})
	padlength=30
	echo "$(printf '%s%*.*s' "$1" 0 $((padlength - ${#1})) "$pad")"
}

account_virtual_boxes() {
	eval "MAILDIR_ACCOUNT_ROOT=${1%/}"
	MAILBOXES_FULL_PATHS="$(echo "$(find $MAILDIR_ACCOUNT_ROOT -name "cur" -type d -exec dirname '{}' \;)" | sort;)"
	for MAILBOX_FULL_PATH in ${MAILBOXES_FULL_PATHS}; do
		notmuch_tag=${MAILBOX_FULL_PATH#$MAILDIR_ACCOUNT_ROOT/}
		# don not add vritual boxes for the default tags
		if [[ ! " ${default_tags[@]} " =~ " ${notmuch_tag} " ]]; then
			result+="\"  ${notmuch_tag}\"                \"notmuch://?query=tag:${2} and tag:${notmuch_tag}\" "
		fi
	done
}

for account_full_path in ~/.mail/*; do
	account_name=$(basename $account_full_path)
	mailbox_name="$(pad_string ${account_name})"
	result+="\"${mailbox_name}\"                \"notmuch://?query=tag:${account_name} and tag:INBOX and not tag:trash\" "
	# add virtual boxes for the default tags
	for tag in "${default_tags[@]}"; do
		result+="\"  ${tag}\"                \"notmuch://?query=tag:${account_name} and tag:${tag}\" "
	done

	account_virtual_boxes ~/.mail/${account_name}/ $account_name
done

echo ${result}
