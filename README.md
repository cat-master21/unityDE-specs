# Unity(X) Shell Fedora RPMs

This repository contains all the RPM spec files needed for
Unity(X) shell which had only been done [once before a long time ago](https://github.com/chenxiaolong/Unity-for-Fedora).
Something that is different is this uses [UnityX](https://unityd.org) ([source code](https://gitlab.com/ubuntu-unity/unity-x)) which is a fork that is maintained and used by [Ubuntu Unity](https://ubuntuunity.org/). This is tested and used on the latest stable version of Fedora. Currently there is only UnityX that works right now but contributions to add Unity 7.7 is helpful.

### RPM spec file progress:
#### Needed for Unityx to build:
* [X] ~~xpathselect-devel~~
* [X] libunity
* [X] libunity-misc-devel
* [X] geis-devel
* [X] glewmx-devel
* [X] nux
* [X] unity-settings-daemon
* [X] ~~compiz9~~
* [X] grail-devel
* [X] frame-devel
* [X] gsettings-ubuntu-touch-schemas
* [X] ~~ido-devel~~
#### Related to Unity but not needed
* [X] vala-panel
* [X] vala-panel-appmenu
* ~~[unity-tweak-tool](https://github.com/freyja-dev/unity-tweak-tool)~~
* ~~unity-control-center~~
* [] unityx-control-center
* [] unityx-power-manager
* ~~unity-greeter~~
* [X] ~~unity-session~~
* [X] ~~ccsm9~~

# Contributing
See [CONTRIBUTING.md](https://github.com/cat-master21/unityDE-specs/blob/main/CONTRIBUTING.md) on how to contribute.
Thanks for spending time to do so!
