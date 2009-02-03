import package

class Package(package.BasePackage):
  def __init__(self, builder):
    package.BasePackage.__init__(self, builder)
    self.url = 'http://busybox.net/downloads/busybox-1.10.1.tar.bz2'
    self.name = 'busybox'
    self.source_file_name = 'busybox-1.10.1.tar.bz2'


  def build(self):
    self.builder.chroot('test', 'pwd')


