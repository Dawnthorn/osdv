import package

class Package(package.BasePackage):
  def __init__(self, builder):
    package.BasePackage.__init__(self, builder)
    self.url = 'ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.0.19.tar.bz2'
    self.name = 'alsa-lib'
    self.source_file_name = 'alsa-lib-1.0.19.tar.bz2'


  def build(self):
    self.builder.chroot('test', 'pwd')


