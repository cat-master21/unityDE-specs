#!/usr/bin/bash

set -x

echo -e "This short script creates virtual RPM packages to make sure that gtk3 and gtk3-devel package requirements are filled while gtk3-ubuntu,\nneeded for Unity is still installed as they conflict."
echo "This uses FPM (https://github.com/jordansissel/fpm) to do so."

#fpm --help > /dev/null || echo "fpm was not found. Use gem install fpm to install." && exit 1

fpm -s empty -t rpm -n gtk3 --depends gtk3-ubuntu --version 99.0.0 -a noarch --description 'This is a virtual package for ubuntu-gtk3, which is used by unity so that there is not any problems'
fpm -s empty -t rpm -n gtk3-devel --depends gtk3-ubuntu-devel --version 99.0.0 -a noarch --description 'This is a virtual package for ubuntu-gtk3, which is used by unity so that there is not any problems'
