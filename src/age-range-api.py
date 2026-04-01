#!/usr/bin/env python3
# should live in /usr/lib/age-verification/age-range-api.py

import asyncio
import getpass
import os
import sys
from datetime import date


from dateutil.relativedelta import relativedelta

from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property
from dbus_next.constants import BusType


from utils import get_dob_file_path, run


class AgeVerification(ServiceInterface):
	def __init__(self):
		super().__init__('com.example.AgeVerification')

	def GetAgeRange(self):
		# must return a string to match with spec interface

		try:
			return dob_to_age_range()
		except Exception:
			# ran out of supported methods to securely read dob
			# no requirement to retrieve dob here
			# may be best to assume 0-13 range anyway?
			# ignoring errors allows the api to be used reliably, which is a functional requirement
			return '0-13'


def dob_to_age_range():
	# Per spec of:
	# * CA (AB 1043)
	# * CO (SB 26-51):
	# 0-<13 -> 0-13
	# 13-<16 -> 13-16
	# 16-<18 -> 16-18
	# >=18 -> 18+

	dob = date.fromisoformat(decrypt_dob_file())
	age = relativedelta(date.today(), dob).years
	age_ranges = [0, 13, 16, 18]

	for i, val in enumerate(age_ranges):
		if age < val:
			return f'{age_ranges[i - 1]}-{val}'

	return '18+'


def decrypt_dob_file():
	password = get_dob_file_password()

	return run([
		['echo', password],
		['openssl', 'aes-256-cbc', '-pbkdf2', '-a', '-d', '-in', get_dob_file_path(os.getuid()), '-pass', 'stdin']
	])


def get_dob_file_password():
	return prompt_for_password(
		'Age range API request',
		'Password for DOB file:',
		'Password for DOB file for age range API requests: '
	)


def prompt_for_password(ui_title, ui_prompt, tty_prompt):
	# https://develop.kde.org/docs/administration/kdialog/
	kdialog_cmd = [[
		'kdialog',
		'--title', ui_title,
		'--password', ui_prompt
	]]

	# https://sourceforge.net/p/yad-dialog/wiki/Examples/
	yad_cmd = [[
		'yad',
		f'--title={ui_title}',
		f'--text={ui_prompt}',
		'--entry',
		'--hide-text'
	]]

	# https://github.com/ncruces/zenity/blob/master/cmd/zenity/main.go
	zenity_cmd = [[
		'zenity',
		'--title', ui_title,
		'--password', ui_prompt
	]]

	for cmd in [kdialog_cmd, yad_cmd, zenity_cmd]:
		try:
			return run(cmd)
		except RuntimeError:
			continue

	if sys.stdin.isatty():
		return getpass.getpass(tty_prompt)

	raise RuntimeError('No supported mechanism to securely get password.')


async def main():
	bus = await MessageBus(bus_type=BusType.SESSION).connect()

	age_verification = AgeVerification()
	bus.export('/com/example/AgeVerification', age_verification)

	await bus.request_name('com.example.AgeVerification')
	await asyncio.Event().wait()


if __name__ == '__main__':
	asyncio.run(main())
