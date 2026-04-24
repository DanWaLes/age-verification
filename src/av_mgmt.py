#!/usr/bin/env python3

import subprocess
import sys
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
	return uid >= MIN_UID and uid < MAX_UI


def is_valid_dob(dob):
	try:
		datetime.strptime(dob, '%Y-%m-%d')
		return True
	except ValueError:
		return False


def set_av_details(uid, region, dob):
	if not is_valid_uid(uid):
		 raise ValueError(f'uid must be at least {MIN_UID} and less than {MAX_UID}; uid = {uid}.')

	if not region in get_regions():
		raise ValueError(f'region {region} is not supported.')

	if not is_valid_dob(dob):
		raise ValueError(f'dob must be a real YYYY-MM-DD date.')

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
	

def get_users():
	users = {}

	with open('/etc/passwd', 'r') as f:
		for line in f:
			parts = line.strip().split(':')
			uid = int(parts[2])

			if is_valid_uid(uid):
				users[uid] = parts[0]

	return users


def get_uid():
	while True:
		try:
			uid = int(input('User ID: ').strip())

			if is_valid_uid(uid):
				return uid

			raise ValueError('')
		except ValueError:
			print('Invalid. Try again.')


def get_region():
	print('To determine which age range brackets are used, you must select which region the user lives in.')

	regions_str = ',\n'.join(f'{i}: {region}' for i, region in enumerate(regions))

	while True:
		try:
			print('Select one of:')
			print(regions_str)

			region_num = int(input('Region number: '))

			return get_regions()[region_num]
		except (ValueError, IndexError):
			print('Invalid. Try again.')


def get_dob():
	while True:
		dob = input('Enter DOB (YYYY-MM-DD): ').strip()

		if is_valid_dob(dob):
			return dob

		print('Invalid. Try again.')


while True:
	try:
		print('Enter an existing user ID.')
		print('Users:')

		for uid, uname in get_users().items():
			print(f'{uid} - {uname}')

			uid = get_uid()
			region = get_region()
			dob = get_dob()

			set_av_details(uid, region, dob)
	except EOFError:
		break
	except KeyboardInterrupt:
		print('')
		sys.exit(0)
