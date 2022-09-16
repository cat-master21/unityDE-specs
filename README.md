# Unity shell RPM specs
This repository contains all the RPM spec files needed for
Unity shell which had only been done [once before a long time ago](https://github.com/chenxiaolong/Unity-for-Fedora). Something that is different is this uses [Unity 7.6](https://gitlab.com/ubuntu-unity/unity/unity) which is a fork that is maintained and used by [Ubuntu Unity](https://ubuntuunity.org/). The RPM specs are tested and used on the latest stable version of Fedora.

### RPM spec file progress:
#### needed for Unity to build:
* [X] xpathselect-devel
* [X] libunity-devel
* [X] libunity-misc-devel
* [] geis-devel
* [] nux-devel
* [] unity-settings-daemon-devel
* [X] compiz9
* [] grail-devel
* [X] frame-devel
#### related to Unity but not needed (especially non devel)
* [X] libunity
* [] xpathselect
* [] libunity-misc
* [] unity-tweak-tool
* [] unity-control-center
* [] unity-control-center-devel
* [] geis
* [] unity-greeter
* [] nux
* [X] ccsm9
* [] unity-settings-daemon
* [] grail
* [] frame

# Contributing
See [CONTRIBUTING.md](https://github.com/cat-master21/unityDE-specs/blob/main/CONTRIBUTING.md) for info on how to contribute. Thanks for spending time to do so!