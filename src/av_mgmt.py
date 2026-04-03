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

	print('A common age range number is used to decide regional age ranges. See README.md for details.')

	car = None

	while True:
		try:
			car = int(input('Enter common age range number (between 0 and 0): '))

			if car >= 0 and car <= 0:
				break
			else:
				print('Invalid. Try again.')
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
			input=f'{car}\n{dob}'.encode(),
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

			uid = int(input('User ID: ').strip())

			set_av_details(uid)
	except EOFError:
		break
	except KeyboardInterrupt:
		sys.exit(0)
