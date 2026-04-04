#!/usr/bin/env python3

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def get_users():
	users = {}

	with open('/etc/passwd', 'r') as f:
		for line in f:
			parts = line.strip().split(':')
			uid = int(parts[2])

			if uid >= 1000 and uid < 65534:
				users[uid] = parts[0]

	return users

users = get_users()

def set_av_details(uid):
	if uid not in users:
		print(f'Could not set age verification details for user {uid}.')
		return

	print('To determine which age range brackets are used, you must select which region you live in.')

	region = None
	regions = [
		'US - CA',
		'US - CO'
	]
	regions_str = ',\n'.join(f"{i}: {region}" for i, region in enumerate(regions))

	while True:
		try:
			print('Select one of:')
			print(regions_str)

			region = int(input('Region number: '))

			if region < 0 or region > len(regions):
				print('Invalid. Try again.')
			else:
				break
		except ValueError:
			print('Invalid. Try again.')

	dob = None

	while True:
		dob = input('Enter DOB (YYYY-MM-DD): ').strip()

		try:
			datetime.strptime(dob, '%Y-%m-%d')
			break
		except ValueError:
			print('Invalid. Try again.')

	print('A password will be needed for securely storing age verification details.')
	print('The user should enter a strong password.')

	av_dir = Path('/etc/age-verification')
	av_dir.mkdir(exist_ok=True)

	try:
		# openssl prompts for password and password confirmation when the program is connected to a terminal

		subprocess.run(
			[
				'openssl', 'aes-256-cbc', '-pbkdf2', '-a',
				'-out', f'{av_dir}/{uid}.enc'
			],
			input=f'{regions[region]}\n{dob}'.encode(),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			check=True
		)

		print(f'Saved age verification details for user {uid}.')
	except subprocess.CalledProcessError as e:
		print(f'Encryption failed: {e.stderr.decode()}')
	except Exception as e:
		print(f'Error: {str(e)}')

while True:
	try:
		print('Enter an existing user ID.')
		print('Users:')

		for uid, uname in users.items():
			print(f'{uid} - {uname}')
			set_av_details(int(input('User ID: ').strip()))
	except EOFError:
		break
	except KeyboardInterrupt:
		print('')
		sys.exit(0)
