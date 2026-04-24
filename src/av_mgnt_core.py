#!/usr/bin/env python3

import subprocess
from datetime import datetime
from pathlib import Path

MIN_UID = 1000
MAX_UID = 65534

def get_regions():
	return [
		'US - CA',
		'US - CO'
	]


def is_valid_uid(uid):
	return uid >= MIN_UID and uid < MAX_UID


def is_valid_dob(dob):
	try:
		datetime.strptime(dob, '%Y-%m-%d')
		return True
	except ValueError:
		return False


def set_av_details(uid, region, dob):
	# TODO pass password as a set_av_details param to openssl 

	if not is_valid_uid(uid):
		 raise ValueError(f'uid must be at least {MIN_UID} and less than {MAX_UID}; uid = {uid}.')

	if not region in get_regions():
		raise ValueError(f'region not supported; region = {region}.')

	if not is_valid_dob(dob):
		raise ValueError(f'dob must be a real YYYY-MM-DD date; dob = {dob}.')

	av_dir = Path('/etc/age-verification')
	av_dir.mkdir(exist_ok=True)

	print('A password will be needed for securely storing age verification details.')
	print('The user should enter a strong password.')

	try:
		# openssl prompts for password and password confirmation when the program is connected to a terminal

		subprocess.run(
			[
				'openssl', 'aes-256-cbc', '-pbkdf2', '-a',
				'-out', f'{av_dir}/{uid}.enc'
			],
			input=f'{region}\n{dob}'.encode(),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			check=True
		)

		print(f'Saved age verification details for user {uid}.')
	except subprocess.CalledProcessError as e:
		print(f'Encryption failed: {e.stderr.decode()}')
	except Exception as e:
		print(f'Error: {str(e)}')	
