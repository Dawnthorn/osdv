import os

class BasePackage:
  def __init__(self, builder):
    self.builder = builder
    self.vars = {}
    self.build_dir = os.path.join('tmp', self.extract_dir)
    self.vars['iso_dir'] = 'iso'
    self.vars['iso_bin_dir'] = os.path.join(self.vars['iso_dir'], 'bin')
    self.vars['iso_boot_dir'] = os.path.join(self.vars['iso_dir'], 'boot')
    self.vars['iso_sbin_dir'] = os.path.join(self.vars['iso_dir'], 'sbin')
    self.vars['iso_usr_bin_dir'] = os.path.join(self.vars['iso_dir'], 'usr', 'bin')
    self.vars['iso_usr_lib_dir'] = os.path.join(self.vars['iso_dir'], 'usr', 'lib')
    self.vars['iso_usr_share_dir'] = os.path.join(self.vars['iso_dir'], 'usr', 'share')
    self.vars['chroot_dir'] = 'chroot'
    self.vars['chroot_bin_dir'] = os.path.join(self.vars['chroot_dir'], 'bin')
    self.vars['chroot_boot_dir'] = os.path.join(self.vars['chroot_dir'], 'boot')
    self.vars['chroot_tmp_dir'] = os.path.join(self.vars['chroot_dir'], 'tmp')
    self.vars['chroot_usr_bin_dir'] = os.path.join(self.vars['chroot_dir'], 'usr', 'bin')
    self.vars['chroot_usr_lib_dir'] = os.path.join(self.vars['chroot_dir'], 'usr', 'lib')
    self.vars['chroot_usr_share_dir'] = os.path.join(self.vars['chroot_dir'], 'usr', 'share')
 


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


  def install(self):
    for install_instruction in self.install_list:
      method = getattr(self, 'install_%s' % (install_instruction[0]))
      method(install_instruction)


  def install_c(self, install_instruction):
    source = install_instruction[1] % self.vars
    target = install_instruction[2] % self.vars
    target_dir_name = os.path.dirname(target)
    self.builder.mkdir(target_dir_name)
    self.builder.sudo('copy-%s-%s' % (source, target), 'cp %s %s' % (source, target))

  def install_d(self, install_instruction):
    source = os.path.join(self.vars['chroot_dir'], install_instruction[1])
    target = os.path.join(self.vars['iso_dir'], install_instruction[1])
    self.builder.mkdir(os.path.dirname(target))
    if not os.path.isfile(source):
      raise Exception("Can only duplicate regular files and '%s' is not a regular file." % source)
    self.builder.sudo('copy-%s-%s' % (source, target), 'cp %s %s' % (source, target))


  def install_l(self, install_instruction):
    source = install_instruction[1] % self.vars
    target = install_instruction[2] % self.vars
    target_dir_name = os.path.dirname(target)
    target_base_name = os.path.basename(target)
    self.builder.sudo('mkdir-%s' % (target_dir_name), 'mkdir -p %s' % (target_dir_name))
    self.builder.sudo('ln-%s-%s' % (source, target), 'sh -c "cd %s && ln -s %s %s"' % (target_dir_name, source, target_base_name))


  def snapshot(self):
    self.builder.sudo('%s-before-snapshot' % self.name, 'find chroot > state/%s-before' % self.name)


  def snapshot_diff(self):
    self.builder.sudo('%s-after-snapshot' % self.name, 'find chroot > state/%s-after' % (self.name))
    self.builder.sudo('%s-snapshot-diff' % self.name, 'diff -u state/%s-before state/%s-after > state/%s-diff' % (self.name, self.name, self.name), None, True)
