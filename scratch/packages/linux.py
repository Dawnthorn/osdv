import package

class Package(package.BasePackage):
  def __init__(self, builder):
    self.url = 'http://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.28.3.tar.bz2'
    self.name = 'linux'
    self.source_file_name = 'linux-2.6.28.3.tar.bz2'
    self.extract_dir = 'linux-2.6.28.3'
    package.BasePackage.__init__(self, builder)
    self.install_list = \
    [
      ['c', '%(chroot_boot_dir)s/vmlinuz-2.6.28.3', '%(iso_boot_dir)s/'],
      ['c', '%(chroot_boot_dir)s/System.map-2.6.28.3', '%(iso_boot_dir)s/'],
      ['c', '%(chroot_boot_dir)s/config-2.6.28.3', '%(iso_boot_dir)s/'],
      ['c', '%(chroot_dir)s/lib/modules/2.6.28.3/kernel/arch/x86/kernel/test_nx.ko', '%(iso_dir)s/lib/modules/2.6.28.3/kernel/arch/x86/kernel/test_nx.ko'],
      ['c', '%(chroot_dir)s/lib/modules/2.6.28.3/kernel/drivers/scsi/scsi_wait_scan.ko', '%(iso_dir)s/lib/modules/2.6.28.3/kernel/drivers/scsi/scsi_wait_scan.ko'],
      ['c', '%(chroot_dir)s/lib/modules/2.6.28.3/kernel/drivers/hid/hid-dummy.ko', '%(iso_dir)s/lib/modules/2.6.28.3/kernel/drivers/hid/hid-dummy.ko'],
      ['c', '%(chroot_dir)s/lib/modules/2.6.28.3/modules.order', '%(iso_dir)s/lib/modules/2.6.28.3/modules.order'],
    ]


  def build(self):
    self.builder.chroot('%s-make-config' % self.name, 'make mrproper', 'tmp/%s' % self.extract_dir)
    self.builder.sudo('%s-copy-config' % self.name, 'cp packages/linux-config chroot/tmp/%s/.config' % self.extract_dir)
    self.builder.chroot('%s-make' % self.name, 'make', 'tmp/%s' % self.extract_dir)
    self.snapshot()
    self.builder.chroot('%s-make-install' % self.name, 'make modules_install install', 'tmp/%s' % self.extract_dir)
    self.snapshot_diff()


