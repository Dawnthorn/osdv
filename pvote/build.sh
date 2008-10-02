#!/bin/sh

. ./vars.sh

if [ ! -d $BUILD_DIR ]; then
  mkdir $BUILD_DIR
fi

cd $BUILD_DIR
if [ ! -e $SOURCE_DIST_FILE ]; then
  wget $SOURCE_DIST_BASE_URL/$SOURCE_DIST_FILE
fi
if [ ! -e $BALLOT_DIST_FILE ]; then
  wget $SOURCE_DIST_BASE_URL/$BALLOT_DIST_FILE
fi
if [ -d $SOURCE_DIR ]; then
  rm -r $SOURCE_DIR
fi
mkdir $SOURCE_DIR
cd $SOURCE_DIR
unzip ../$SOURCE_DIST_FILE
unzip ../$BALLOT_DIST_FILE
cd ..
cp -r debian $SOURCE_DIR
cd $SOURCE_DIR
dpkg-buildpackage -rfakeroot
