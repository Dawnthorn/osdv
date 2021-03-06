#!/usr/bin/env python

import os
import select
import subprocess
import sys

def run(command):
  print command
  process = subprocess.Popen(command, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, close_fds = True, bufsize = 0)
  process.stdin.close()
  done = False
  while not done:
    result = select.select([process.stdout, process.stderr], [], [], 1)
    if len(result[0]) > 0:
      for file in result[0]:
	if file == process.stdout:
	  data = file.readline()
	  if data == '':
	    done = True
	  sys.stdout.write(data)
	else:
	  data = file.readline()
	  if data == '':
	    done = True
	  sys.stderr.write(data)
    else:
      result = os.waitpid(process.pid, os.WNOHANG)
      if result[0] != 0 or result[1] != 0:
	done = True
    result = select.select([process.stdout, process.stderr], [], [], 1)
    for file in result[0]:
      if file == process.stdout:
	sys.stdout.write(file.readline())
      else:
	sys.stderr.write(file.readline())

