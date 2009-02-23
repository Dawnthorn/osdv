import os
import package

class Package(package.BasePackage):
  def __init__(self, builder):
    self.url = 'http://busybox.net/downloads/busybox-1.10.1.tar.bz2'
    self.name = 'busybox'
    self.source_file_name = 'busybox-1.10.1.tar.bz2'
    self.extract_dir = 'busybox-1.10.1'
    package.BasePackage.__init__(self, builder)
    self.vars['busybox_install_dir'] = os.path.join(self.vars['chroot_tmp_dir'], self.extract_dir, '_install')
    self.vars['busybox_install_bin_dir'] = os.path.join(self.vars['busybox_install_dir'], 'bin')
    self.install_list = \
    [
      ['c', "%(busybox_install_bin_dir)s/busybox", "%(iso_bin_dir)s/busybox"],
      ['l', "busybox", "%(iso_bin_dir)s/ash"],
      ['l', "busybox", "%(iso_bin_dir)s/echo"],
      ['l', "busybox", "%(iso_bin_dir)s/sh"],
      ['l', "../../bin/busybox", "%(iso_usr_bin_dir)s/test"],
      ['l', "../../bin/busybox", "%(iso_usr_bin_dir)s/["],
      ['l', "../../bin/busybox", "%(iso_usr_bin_dir)s/[["],
      ['l', "../bin/busybox", "%(iso_sbin_dir)s/init"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/chmod"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/chown"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/ln"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/ls"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/mknod"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/mv"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/rm"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/sed"],
      ['l', "../bin/busybox", "%(iso_bin_dir)s/uname"],
    ]


  def build(self):
    self.builder.sudo('%s-copy-config' % self.name, 'cp packages/busybox-config chroot/tmp/%s/.config' % self.extract_dir)
    self.builder.chroot('%s-make' % self.name, 'make', 'tmp/%s' % self.extract_dir)
    self.snapshot()
    self.builder.chroot('%s-make-install' % self.name, 'make install', 'tmp/%s' % self.extract_dir)
    self.snapshot_diff()
 

