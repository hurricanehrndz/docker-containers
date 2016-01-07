#!/bin/bash

ignored_folders=("INBOX" "flagged" "important" "sent" "drafts" "archive" "trash" "spam" "cur" "new" "tmp")
result=""

pad_account_name() {
	pad=$(printf '%0.1s' "="{1..60})
	padlength=30
	padded_name=$(printf '%s%*.*s' "$1" 0 $((padlength - ${#1})) "$pad")
	result+="+${padded_name} "
}

sub_folders() {
	for sub_d in $(find $1 -mindepth 1 -maxdepth 1 -type d | sort); do
		child_dir=$(basename $sub_d)
		if [[ ! " ${ignored_folders[@]} " =~ " ${child_dir} " ]]; then
			result+="+${2}/${sub_d#~/.mail/$2/} "
		fi
		sub_folders $sub_d $2
	done
}

for d in ~/.mail/*; do
	default_folders=("INBOX" "flagged" "important" "sent" "drafts" "archive" "trash" "spam")
	account_name=$(basename $d)
	pad_account_name ${account_name}
	for f in "${default_folders[@]}"; do
		result+="+${account_name}/${f} "
	done

	sub_folders ~/.mail/${account_name}/ $account_name
done

echo $result
