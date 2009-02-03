import package

class Package(package.BasePackage):
  def __init__(self, builder):
    package.BasePackage.__init__(self, builder)
    self.url = 'http://www.libsdl.org/release/SDL-1.2.13.tar.gz'
    self.name = 'SDL'
    self.source_file_name = 'SDL-1.2.13.tar.gz'


  def build(self):
    self.builder.chroot('test', 'pwd')


