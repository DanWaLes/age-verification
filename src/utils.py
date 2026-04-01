#!/usr/bin/env python3
# should live in /usr/lib/age-verification/utils.py

import subprocess

def get_dob_file_path(uid):
	# uid from os.getuid()
	# os.getuid() returns 0 if running as root
	# value is expected to be >= 1000

	return os.path.abspath(f'/etc/ageverification/{uid}-dob.enc')


def run(commands):
	result = subprocess.run(commands[0], capture_output = True, text = True)

	if result.returncode != 0:
		raise RuntimeError(f"Command failed: {result.stderr}")

	for i in range(1, len(commands)):
		result = subprocess.run(commands[i], input = result.stdout, capture_output = True, text = True)

		if result.returncode != 0:
			raise RuntimeError(f"Command failed: {result.stderr}")

	return result.stdout.strip()
