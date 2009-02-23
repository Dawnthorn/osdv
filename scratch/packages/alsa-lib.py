import os
import package

class Package(package.BasePackage):
  def __init__(self, builder):
    self.url = 'ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.0.19.tar.bz2'
    self.name = 'alsa-lib'
    self.source_file_name = 'alsa-lib-1.0.19.tar.bz2'
    self.extract_dir = 'alsa-lib-1.0.19'
    package.BasePackage.__init__(self, builder)
    self.vars['chroot_smixer_lib_dir'] = os.path.join(self.vars['chroot_usr_lib_dir'], 'alsa-lib', 'smixer')
    self.vars['iso_smixer_lib_dir'] = os.path.join(self.vars['iso_usr_lib_dir'], 'alsa-lib', 'smixer')
    self.install_list = \
    [
      ['d', 'usr/bin/aserver'],
      ['d', 'usr/lib/libasound.la'],
      ['d', 'usr/lib/alsa-lib/smixer/smixer-ac97.la'],
      ['d', 'usr/lib/alsa-lib/smixer/smixer-ac97.so'],
      ['d', 'usr/lib/alsa-lib/smixer/smixer-sbase.so'],
      ['d', 'usr/lib/alsa-lib/smixer/smixer-hda.la'],
      ['d', 'usr/lib/alsa-lib/smixer/smixer-sbase.la'],
      ['d', 'usr/lib/alsa-lib/smixer/smixer-hda.so'],
      ['d', 'usr/lib/libasound.so.2.0.0'],
      ['d', 'usr/lib/libasound.so.2'],
      ['d', 'usr/lib/libasound.so'],
      ['d', 'usr/share/alsa/pcm/front.conf'],
      ['d', 'usr/share/alsa/pcm/surround50.conf'],
      ['d', 'usr/share/alsa/pcm/surround40.conf'],
      ['d', 'usr/share/alsa/pcm/modem.conf'],
      ['d', 'usr/share/alsa/pcm/surround51.conf'],
      ['d', 'usr/share/alsa/pcm/center_lfe.conf'],
      ['d', 'usr/share/alsa/pcm/surround41.conf'],
      ['d', 'usr/share/alsa/pcm/rear.conf'],
      ['d', 'usr/share/alsa/pcm/dsnoop.conf'],
      ['d', 'usr/share/alsa/pcm/iec958.conf'],
      ['d', 'usr/share/alsa/pcm/surround71.conf'],
      ['d', 'usr/share/alsa/pcm/hdmi.conf'],
      ['d', 'usr/share/alsa/pcm/side.conf'],
      ['d', 'usr/share/alsa/pcm/dmix.conf'],
      ['d', 'usr/share/alsa/pcm/dpl.conf'],
      ['d', 'usr/share/alsa/pcm/default.conf'],
      ['d', 'usr/share/alsa/smixer.conf'],
      ['d', 'usr/share/alsa/alsa.conf'],
      ['d', 'usr/share/alsa/cards/CMI8738-MC6.conf'],
      ['d', 'usr/share/alsa/cards/PC-Speaker.conf'],
      ['d', 'usr/share/alsa/cards/ICE1724.conf'],
      ['d', 'usr/share/alsa/cards/CMI8738-MC8.conf'],
      ['d', 'usr/share/alsa/cards/aliases.conf'],
      ['d', 'usr/share/alsa/cards/AU8830.conf'],
      ['d', 'usr/share/alsa/cards/Audigy.conf'],
      ['d', 'usr/share/alsa/cards/USB-Audio.conf'],
      ['d', 'usr/share/alsa/cards/VIA8237.conf'],
      ['d', 'usr/share/alsa/cards/VXPocket.conf'],
      ['d', 'usr/share/alsa/cards/RME9636.conf'],
      ['d', 'usr/share/alsa/cards/CMI8338-SWIEC.conf'],
      ['d', 'usr/share/alsa/cards/ICH4.conf'],
      ['d', 'usr/share/alsa/cards/Audigy2.conf'],
      ['d', 'usr/share/alsa/cards/CA0106.conf'],
      ['d', 'usr/share/alsa/cards/PMacToonie.conf'],
      ['d', 'usr/share/alsa/cards/SI7018.conf'],
      ['d', 'usr/share/alsa/cards/ATIIXP-SPDMA.conf'],
      ['d', 'usr/share/alsa/cards/VIA8233.conf'],
      ['d', 'usr/share/alsa/cards/ENS1370.conf'],
      ['d', 'usr/share/alsa/cards/ICH-MODEM.conf'],
      ['d', 'usr/share/alsa/cards/PS3.conf'],
      ['d', 'usr/share/alsa/cards/ATIIXP-MODEM.conf'],
      ['d', 'usr/share/alsa/cards/ENS1371.conf'],
      ['d', 'usr/share/alsa/cards/HDA-Intel.conf'],
      ['d', 'usr/share/alsa/cards/VX222.conf'],
      ['d', 'usr/share/alsa/cards/aliases.alisp'],
      ['d', 'usr/share/alsa/cards/CMI8788.conf'],
      ['d', 'usr/share/alsa/cards/EMU10K1X.conf'],
      ['d', 'usr/share/alsa/cards/SI7018/sndoc-mixer.alisp'],
      ['d', 'usr/share/alsa/cards/SI7018/sndop-mixer.alisp'],
      ['d', 'usr/share/alsa/cards/AACI.conf'],
      ['d', 'usr/share/alsa/cards/ATIIXP.conf'],
      ['d', 'usr/share/alsa/cards/PMac.conf'],
      ['d', 'usr/share/alsa/cards/RME9652.conf'],
      ['d', 'usr/share/alsa/cards/Aureon51.conf'],
      ['d', 'usr/share/alsa/cards/VIA686A.conf'],
      ['d', 'usr/share/alsa/cards/AU8820.conf'],
      ['d', 'usr/share/alsa/cards/FM801.conf'],
      ['d', 'usr/share/alsa/cards/CMI8338.conf'],
      ['d', 'usr/share/alsa/cards/YMF744.conf'],
      ['d', 'usr/share/alsa/cards/ICE1712.conf'],
      ['d', 'usr/share/alsa/cards/TRID4DWAVENX.conf'],
      ['d', 'usr/share/alsa/cards/CS46xx.conf'],
      ['d', 'usr/share/alsa/cards/EMU10K1.conf'],
      ['d', 'usr/share/alsa/cards/VIA8233A.conf'],
      ['d', 'usr/share/alsa/cards/ICH.conf'],
      ['d', 'usr/share/alsa/cards/ES1968.conf'],
      ['d', 'usr/share/alsa/cards/VXPocket440.conf'],
      ['d', 'usr/share/alsa/cards/Maestro3.conf'],
      ['d', 'usr/share/alsa/cards/GUS.conf'],
      ['d', 'usr/share/alsa/cards/AU8810.conf'],
      ['d', 'usr/share/alsa/cards/NFORCE.conf'],
      ['d', 'usr/share/alsa/cards/Aureon71.conf'],
      ['d', 'usr/share/alsa/sndo-mixer.alisp'],
    ]


  def build(self):
    self.builder.chroot('%s-configure' % self.name, './configure', self.build_dir)
    self.builder.chroot('%s-make' % self.name, 'make', self.build_dir)
    self.snapshot()
    self.builder.chroot('%s-make-install' % self.name, 'make install', self.build_dir)
    self.snapshot_diff()


