#!/usr/bin/env python3

import subprocess

def run(commands):
	result = subprocess.run(commands[0], capture_output = True, text = True)

	if result.returncode != 0:
		raise RuntimeError(f"Command failed: {result.stderr}")

	for i in range(1, len(commands)):
		result = subprocess.run(commands[i], input = result.stdout, capture_output = True, text = True)

		if result.returncode != 0:
			raise RuntimeError(f"Command failed: {result.stderr}")

	return result.stdout.strip()
