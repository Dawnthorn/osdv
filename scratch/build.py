#!/usr/bin/env python

import imp
import os
import sys
import watchcmd

sys.path.insert(0, 'packages')

class Builder:
  def run(self, name, command, dir_name = None, ignore_result = False):
    if not os.path.exists('state'):
      os.mkdir('state')
    stamp_file_name = 'state/.%s-done' % name
    if os.path.exists(stamp_file_name):
      return
    if dir_name is not None:
      if os.path.exists(dir_name):
	watchcmd.run('sudo rm -rf %s' % dir_name)
    watchcmd.run(command, ignore_result)
    file = open(stamp_file_name, 'w')
    file.close()


  def sudo(self, name, command, dir_name = None, ignore_result = False):
    self.run(name, 'sudo %s' % command, dir_name, ignore_result)


  def chroot(self, name, command, dir_name = None, ignore_result = False):
    self.sudo(name, "chroot chroot /bin/bash -c 'cd %s && %s'" % (dir_name, command), None, ignore_result)



def load_module(source_file_name):
  try:
    return sys.modules[source_file_name]
  except KeyError:
    pass
  fp, pathname, description = imp.find_module(source_file_name)
  try:
    return imp.load_module(source_file_name, fp, pathname, description)
  finally:
    if fp:
      fp.close()



package_names = \
[
    'module-init-tools',
    'linux',
#    'busybox',
#    'alsa-lib',
#    'sdl',
#    'python',
#    'pygame',
]
  
builder = Builder()
builder.sudo('create-chroot', 'debootstrap --variant=buildd lenny chroot', 'chroot')
for package_name in package_names:
  module = load_module(package_name)
  package = module.Package(builder)
  package.fetch()
  package.copy()
  package.extract()
  package.build()

builder.sudo('make-iso-dir', 'mkdir iso', 'iso')
builder.sudo('make-grub-dir', 'mkdir -p iso/boot/grub')
builder.sudo('copy-stage2', 'cp /usr/lib/grub/i386-pc/stage2_eltorito iso/boot/grub')
builder.sudo('copy-menu-lst', 'cp packages/menu.lst iso/boot/grub')
module = load_module('linux')
package = module.Package(builder)
for file_name in package.install_file_names:
  source_name = 'chroot%s' % file_name
  target_name = 'iso%s' % file_name
  target_dir_name = os.path.dirname(target_name)
  if not os.path.exists(target_dir_name):
    builder.sudo('mkdir-%s' % target_dir_name.replace('/', '_'), 'mkdir -p %s' % target_dir_name)
  if os.path.isdir(source_name):
    if not os.path.exists(target_name):
      builder.sudo('mkdir-%s' % file_name.replace('/', '_'), 'mkdir -p %s' % file_name)
  else:
    builder.sudo('copy-%s' % os.path.basename(file_name), 'cp %s %s' % (source_name, target_name))
builder.sudo('make-dev-dir', 'mkdir iso/dev')
builder.sudo('make-proc-dir', 'mkdir iso/proc')
builder.sudo('make-etc-dir', 'mkdir iso/etc')
builder.sudo('make-sbin-dir', 'mkdir iso/sbin')
builder.sudo('make-bin-dir', 'mkdir iso/bin')
builder.sudo('make-mnt-dir', 'mkdir iso/mnt')
builder.sudo('make-usr-dir', 'mkdir iso/usr')
builder.sudo('make-iso', 'mkisofs -R -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table -o osdv.iso iso')
