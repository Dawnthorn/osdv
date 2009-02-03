import package

class Package(package.BasePackage):
  def __init__(self, builder):
    package.BasePackage.__init__(self, builder)
    self.url = 'http://www.pygame.org/ftp/pygame-1.8.1release.tar.gz'
    self.name = 'pygame'
    self.source_file_name = 'pygame-1.8.1release.tar.gz'


  def build(self):
    self.builder.chroot('test', 'pwd')


