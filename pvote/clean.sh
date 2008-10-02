#!/bin/sh

. ./vars.sh

if [ -d $BUILD_DIR ]; then
  rm -r $BUILD_DIR
fi
