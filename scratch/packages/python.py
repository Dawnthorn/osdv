import package

class Package(package.BasePackage):
  def __init__(self, builder):
    package.BasePackage.__init__(self, builder)
    self.url = 'http://www.python.org/ftp/python/2.6.1/Python-2.6.1.tar.bz2'
    self.name = 'python'
    self.source_file_name = 'Python-2.6.1.tar.bz2'


  def build(self):
    self.builder.chroot('test', 'pwd')


