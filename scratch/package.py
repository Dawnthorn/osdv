import os

class BasePackage:
  def __init__(self, builder):
    self.builder = builder


  def copy(self):
    self.builder.run('copy-%s' % self.name, 'cp sources/%s chroot/tmp' % self.source_file_name)


  def extract(self):
    root, ext = os.path.splitext(self.source_file_name)
    if ext == '.bz2':
      type_flag = 'j'
    else:
      type_flag = 'z'
    self.builder.chroot('extract-%s' % self.name, 'tar -x%sf %s' % (type_flag, self.source_file_name), 'tmp')


  def fetch(self):
    if not os.path.exists('sources'):
      os.mkdir('sources')
    target_file = 'sources/%s' % self.source_file_name
    self.builder.run('fetch-%s' % self.name, 'wget -o wget.log -c -O %s %s' % (target_file, self.url))


  def snapshot(self):
    self.builder.sudo('%s-before-snapshot' % self.name, 'find chroot > state/%s-before' % self.name)


  def snapshot_diff(self):
    self.builder.sudo('%s-after-snapshot' % self.name, 'find chroot > state/%s-after' % (self.name))
    self.builder.sudo('%s-snapshot-diff' % self.name, 'diff -u state/%s-before state/%s-after > state/%s-diff' % (self.name, self.name, self.name), None, True)
