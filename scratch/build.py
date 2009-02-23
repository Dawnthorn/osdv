#!/usr/bin/env python

import imp
import os
import sys
import watchcmd

sys.path.insert(0, 'packages')

class Builder:
  def chroot(self, name, command, dir_name = None, ignore_result = False):
    self.sudo(name, "chroot chroot /bin/bash -c 'cd %s && %s'" % (dir_name, command), None, ignore_result)


  def copy(self, source, target):
    target_dir_name = os.path.dirname(target)
    self.mkdir(target_dir_name)
    self.sudo('copy-%s-%s' % (source, target), 'cp %s %s' % (source, target))


  def mkdir(self, dir_name):
    if not os.path.exists(dir_name):
      self.sudo('mkdir-%s' % dir_name, 'mkdir -p %s' % (dir_name))


  def mknod(self, node_name, type, major, minor):
    self.sudo('mknod-%s-%s-%i-%i' % (node_name, type, major, minor), "chroot iso /bin/sh -c 'cd /dev && mknod %s %s %i %i'" % (node_name, type, major, minor))


  def run(self, name, command, dir_name = None, ignore_result = False):
    if not os.path.exists('state'):
      os.mkdir('state')
    name = name.replace('/', '_')
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
    'busybox',
    'alsa-lib',
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
builder.sudo('make-dev-dir', 'mkdir iso/dev')
builder.sudo('make-proc-dir', 'mkdir iso/proc')
builder.sudo('make-etc-dir', 'mkdir iso/etc')
builder.sudo('make-sbin-dir', 'mkdir iso/sbin')
builder.sudo('make-bin-dir', 'mkdir iso/bin')
builder.sudo('make-mnt-dir', 'mkdir iso/mnt')
builder.sudo('make-usr-dir', 'mkdir iso/usr')
builder.mkdir('iso/lib')
builder.copy('chroot/lib/libc.so.6', 'iso/lib/')
builder.copy('chroot/lib/ld-linux.so.2', 'iso/lib/')
builder.copy('packages/passwd', 'iso/etc/')
builder.copy('packages/shadow', 'iso/etc/')
builder.copy('packages/group', 'iso/etc/')
builder.copy('packages/rcS', 'iso/etc/init.d/')
builder.sudo('make-usr-dir', 'mkdir iso/usr')
builder.mknod('console', 'c', 5, 1)
builder.mknod('tty0', 'c', 4, 0)
builder.mknod('tty1', 'c', 4, 1)
builder.mknod('tty2', 'c', 4, 2)
builder.mknod('tty3', 'c', 4, 3)
builder.mknod('tty4', 'c', 4, 4)
builder.mknod('tty5', 'c', 4, 5)
builder.mknod('tty6', 'c', 4, 6)
builder.mknod('tty7', 'c', 4, 7)


for package_name in package_names:
  module = load_module(package_name)
  package = module.Package(builder)
  package.install()
builder.sudo('make-iso', 'mkisofs -R -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table -o osdv.iso iso')
