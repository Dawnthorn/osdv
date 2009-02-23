#!/usr/bin/env python

import os
import select
import subprocess
import sys

class WatchcmdException(Exception):
  pass

def run(command, ignore_result = False):
  print command
  process = subprocess.Popen(command, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, close_fds = True, bufsize = 0)
  process.stdin.close()
  child_result = None
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
	child_result = result[1]
	done = True
  if child_result is None:
    child_result = process.wait()
  if not ignore_result:
    if child_result != 0:
      raise WatchcmdException("Execution of '%s' failed with return code %d." % (command, child_result))
  return child_result

