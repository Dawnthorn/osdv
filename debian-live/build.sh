#!/bin/sh

PVOTE_PACKAGE_DIR=../pvote
PVOTE_PACKAGE_FILE=$PVOTE_PACKAGE_DIR/build/pvote_1.0b-1_all.deb
if [ ! -e $PVOTE_PACKAGE_FILE ]; then
  cd $PVOTE_PACKAGE_DIR
  ./build.sh
  cd ../debian-live
fi

cp $PVOTE_PACKAGE_FILE config/chroot_local-packages

sudo lh_build
