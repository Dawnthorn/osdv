#!/usr/bin/env python

import os.path
import re
import shutil
import sys
import urllib
import watchcmd

chroot_dir = 'build-chroot'
chroot_tmp_dir = 'tmp'
chroot_work_dir = os.path.join(chroot_tmp_dir, 'work')
ext_chroot_tmp_dir = os.path.join(chroot_dir, chroot_tmp_dir)
ext_chroot_work_dir = os.path.join(chroot_dir, chroot_work_dir)
build_base_dir = 'build'
built_package_dir = os.path.join('build', 'built-packages')

file_names_to_copy = \
[
  'watchcmd.py',
  'build-package.py',
]

def build_package(package_name):
  watchcmd.run('chroot %s python -u /tmp/build-package.py %s' % (chroot_dir, package_name))

def cache_packages():
  if os.path.exists('cache/packages_bootstrap'):
    watchcmd.run('rm -rf cache/packages_bootstrap')
  os.makedirs('cache/packages_bootstrap')
  watchcmd.run('cp %s/var/cache/apt/archives/*.deb cache/packages_bootstrap' % (chroot_dir))

def restore_packages():
  apt_archive_dir = '%s/var/cache/apt/archives' % (chroot_dir)
  if not os.path.exists(apt_archive_dir):
    os.makedirs(apt_archive_dir)
  watchcmd.run('cp cache/packages_bootstrap/*.deb %s/var/cache/apt/archives' % (chroot_dir))

def configure_sources():
  sources_file = open('%s/etc/apt/sources.list' % chroot_dir)
  for line in sources_file.readlines():
    if line.startswith('deb-src'):
      return
  sources_file.close()
  source_file = open('%s/etc/apt/sources.list' % chroot_dir, 'a')
  source_file.write("\ndeb-src http://ftp.debian.org/debian lenny main contrib non-free\n")
  source_file.close()
  watchcmd.run("chroot %s apt-get update" % chroot_dir)


def build_packages():
  watchcmd.run("chroot %s apt-get update" % chroot_dir)
  watchcmd.run("chroot %s apt-get -y install apt-utils" % chroot_dir)
  watchcmd.run("chroot %s apt-get -y install build-essential" % chroot_dir)
  watchcmd.run("chroot %s apt-get -y install dpkg-dev" % chroot_dir)
  watchcmd.run("chroot %s apt-get -y install fakeroot" % chroot_dir)
  watchcmd.run("chroot %s apt-get -y install python-minimal" % chroot_dir)
  watchcmd.run("chroot %s apt-get -y install squashfs-tools" % chroot_dir)
  watchcmd.run("reprepro -V -b repro includedeb osdv build-chroot/var/cache/apt/archives/squashfs-tools_1%3a3.3-7_i386.deb")
  watchcmd.run("chroot %s apt-get -y install genisoimage" % chroot_dir)
  watchcmd.run("reprepro -V -b repro includedeb osdv build-chroot/var/cache/apt/archives/genisoimage_9%3a1.1.9-1_i386.deb")


package_name = None
if len(sys.argv) > 1:
  package_name = sys.argv[1]

try:
  restore_packages()
  if not os.path.exists('.stage_build_chroot'):
    watchcmd.run('debootstrap --download-only --verbose --variant buildd lenny %s http://ftp.debian.org/debian' % (chroot_dir))
    cache_packages()
    watchcmd.run('debootstrap --verbose --variant buildd lenny %s http://ftp.debian.org/debian' % (chroot_dir))
    build_packages()
    watchcmd.run('touch .stage/build_chroot')
  configure_sources()
  restore_packages()
  manifest_file_name = 'build/manifest'
  manifest_file = open(manifest_file_name)
  for file_name in file_names_to_copy:
    shutil.copyfile(os.path.join(build_base_dir, file_name), os.path.join(ext_chroot_tmp_dir, file_name))
  watchcmd.run('cp -r patches %s' % (ext_chroot_tmp_dir))
  if package_name is None:
    file_names = os.listdir('patches')
    for file_name in file_names:
      package_name = os.path.splitext(file_name)[0]
      build_package(package_name)
  else:
    build_package(package_name)
  if not os.path.exists(built_package_dir):
    os.makedirs(built_package_dir)
  watchcmd.run('cp %s/*.deb %s' % (ext_chroot_work_dir, built_package_dir))
  built_package_names = os.listdir(built_package_dir)
  matcher = re.compile('_.*')
  for built_package_name in built_package_names:
    package_name = matcher.sub('', built_package_name)
    watchcmd.run('reprepro -Vb repro remove osdv %s' % (package_name))
    watchcmd.run('reprepro -Vb repro includedeb osdv %s/%s' % (built_package_dir, built_package_name))
    for root, dirs, file_names in os.walk('cache'):
      for file_name in file_names:
	if package_name == file_name:
	  os.unlink(os.path.join(root, file_name))
finally:
  cache_packages()
  for file_name in file_names_to_copy:
    file_path = os.path.join(ext_chroot_tmp_dir, file_name)
    if os.path.exists(file_path):
      os.unlink(file_path)

