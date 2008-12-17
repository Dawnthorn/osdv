#!/usr/bin/env python

import os
import re
import sys

sys.path.append('build')
import watchcmd

watchcmd.run('cp config/bootstrap.orig config/bootstrap')
pvote_package_dir = '../pvote'
pvote_package_file = os.path.join(pvote_package_dir, 'build/pvote_1.0b-1_all.deb')
if not os.path.exists(pvote_package_file):
  os.chdir(pvote_package_dir)
  watchcmd.run('./build.sh')
  os.chdir('../debian-live')

watchcmd.run('cp %s config/chroot_local-packages' % (pvote_package_file))
watchcmd.run('sudo lh_bootstrap')
watchcmd.run('sudo lh_chroot')

def import_packages():
  for root, dirs, files in os.walk('cache'):
    for file_name in files:
      file_path = os.path.join(root, file_name)
      if not file_path.endswith('.deb'):
	continue
      watchcmd.run('reprepro -V -b repro includedeb osdv %s' % file_path)

import_packages()

def create_local_bootstrap(chroot = False):
  local_bootstrap_file = open('config/bootstrap.local')
  bootstrap_file = open('config/bootstrap', 'w')
  current_dir = os.getcwd()
  if chroot:
    bootstrap_repro_dir = 'file:///repro'
    repro_dir = 'file:///repro'
  else:
    bootstrap_repro_dir = 'file:///%s/repro' % (current_dir)
    repro_dir = 'file:///repro'
  for line in local_bootstrap_file.readlines():
    bootstrap_matcher = re.compile('%local_bootstrap_repro%')
    matcher = re.compile('%local_repro%')
    line = matcher.sub(repro_dir, line)
    line = bootstrap_matcher.sub(bootstrap_repro_dir, line)
    bootstrap_file.write(line)

create_local_bootstrap()
watchcmd.run('sudo python -u ./build/build-packages.py')
watchcmd.run("sudo bash -c 'cd /usr/share/debootstrap/scripts && rm -f osdv && ln -s lenny osdv'")
watchcmd.run('sudo lh_clean')
watchcmd.run('sudo lh_bootstrap')
watchcmd.run('sudo cp -r ~/.gnupg/pubring.gpg chroot/tmp')
watchcmd.run('sudo chroot chroot apt-key add /tmp/pubring.gpg')
watchcmd.run('sudo cp -r repro chroot/repro')
watchcmd.run('sudo chroot chroot apt-get update')
create_local_bootstrap(True)
watchcmd.run('sudo lh_chroot')
watchcmd.run('sudo lh_binary')
watchcmd.run('sudo lh_source')
watchcmd.run('sudo rm -rf chroot/repro')
