import package

class Package(package.BasePackage):
  def __init__(self, builder):
    package.BasePackage.__init__(self, builder)
    self.url = 'http://www.kernel.org/pub/linux/utils/kernel/module-init-tools/module-init-tools-3.5.tar.bz2'
    self.name = 'module-init-tools'
    self.source_file_name = 'module-init-tools-3.5.tar.bz2'
    self.extract_dir = 'module-init-tools-3.5'


  def build(self):
    self.builder.chroot('%s-configure' % self.name, './configure', 'tmp/%s' % self.extract_dir)
    self.builder.chroot('%s-make' % self.name, 'make', 'tmp/%s' % self.extract_dir)
    self.builder.chroot('%s-make-install' % self.name, 'make install', 'tmp/%s' % self.extract_dir)


