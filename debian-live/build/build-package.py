#!/usr/bin/env python

import os
import select
import subprocess
import sys
import watchcmd

package_name = sys.argv[1]

if not os.path.exists('/tmp/work'):
  os.mkdir('/tmp/work')
os.chdir('/tmp/work')
watchcmd.run('rm -rf %s*' % (package_name))
watchcmd.run('apt-get -y build-dep %s' % (package_name))
watchcmd.run('apt-get -y source %s' % (package_name))
file_names = os.listdir('/tmp/work')
for file_name in file_names:
  if os.path.isdir(file_name) and file_name.startswith(package_name):
    source_dir_name = file_name
os.chdir(source_dir_name)
print os.getcwd()
patch_file_name = '/tmp/patches/%s.patch' % (package_name)
if os.path.exists(patch_file_name):
  watchcmd.run('patch -p0 < %s' % (patch_file_name))
watchcmd.run('dpkg-buildpackage -rfakeroot')
