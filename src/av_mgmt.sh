#!/usr/bin/env bash

users=$(awk -F: '$3 >= 1000 && $3 < 65534 {print $1, $3}' /etc/passwd)
uids=$(awk -F: '$3 >= 1000 && $3 < 65534 {print $3}' /etc/passwd)

set_av_details() {
	uid="$1"

	if ! echo "$uids" | grep -qw "^$uid"; then
		echo "Could not set age verification details for user $uid."
		return
	fi

	# public IP and clock/region/language not used decide car because it doesnt account for being abroad
	echo "A common age range number is used to decide regonal age ranges should be used. See README.md for details."
	
	while true; do
		read -r -p "Enter common age range number (between 0 and 0): " car
		if [[ "$car" =~ ^[0-9]+$ ]] && (( car >= 0 && car <= 0 )); then
			break
		else
			echo "Invalid. Try again."
		fi
	done

	while true; do
		read -r -p "Enter DOB (YYYY-MM-DD): " dob

		if date -d "$dob" "+%Y-%m-%d" >/dev/null 2>&1; then
			break
		else
			echo "Invalid. Try again."
		fi
	done

	echo "A password will be needed for securely storing DOB"
	echo "This password should be shared with the user"

	mkdir -p /etc/ageverification

	echo -n "$car\n$dob" | \
	openssl aes-256-cbc -pbkdf2 -a -out "/etc/ageverification/${uid}.enc"

	echo "Set age verification details for user $uid"
}

while true; do
	echo "Enter an existing user ID"
	echo "Users:"
	echo "$users"

	read -r uid

	set_av_details "$uid"
done
