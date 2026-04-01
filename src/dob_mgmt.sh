#!/usr/bin/env bash
# should live in /usr/lib/age-verification/dob_mgmt.sh

users=$(awk -F: '$3 >= 1000 && $3 < 65534 {print $1, $3}' /etc/passwd)
uids=$(awk -F: '$3 >= 1000 && $3 < 65534 {print $3}' /etc/passwd)

set_dob() {
	uid="$1"

	if ! echo "$uids" | grep -qw "^$uid"; then
		echo "Could not set DOB for user $uid."
		return
	fi

	while true; do
		read -r -p "Enter DOB (YYYY-MM-DD): " date_input

		if date -d "$date_input" "+%Y-%m-%d" >/dev/null 2>&1; then
			break
		else
			echo "Invalid format. Please use YYYY-MM-DD."
		fi
	done

	echo "A password will be needed for securely storing DOB"
	echo "This password should be shared with the user"

	mkdir -p /etc/ageverification

	echo -n date_input | \
	openssl aes-256-cbc -pbkdf2 -a -out "/etc/ageverification/${uid}"-dob.enc

	echo "Set DOB for user $uid"
}

while true; do
	echo "Enter an existing user ID"
	echo "Users:"
	echo "$users"

	read -r uid

	set_dob "$uid"
done
