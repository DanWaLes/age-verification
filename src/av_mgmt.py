#!/usr/bin/env python3

import sys

# https://askubuntu.com/questions/470982/how-to-add-a-python-module-to-syspath
sys.path.insert(0, '/usr/lib/age-verification')
from av_mgnt_core import get_regions, is_valid_uid, is_valid_dob, set_av_details

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

	regions_str = ',\n'.join(f'{i}: {region}' for i, region in enumerate(get_regions()))

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
