This Directory contains patches, either modifications to spec files or sources.

* `add-files-to-meson.patch` Ubuntu's patches for gtk3 create new files and applies it's files to autoconfig but not to meson which Fedora uses. This is a patch for [gtk3.spec](https://src.fedoraproject.org/rpms/gtk3/blob/rawhide/f/gtk3.spec)

* `gtk3-ubuntu.patch` Ubuntu adds files to it's gtk3 (`ubuntu-private.h`, `ubuntumenuitemfactory.h`, etc) and other patches used specifically for Unity and is required for some packages (`ido` for example). This patch should be reapplied every once and awhile. This is a patch for [gtk3 spec](https://src.fedoraproject.org/rpms/gtk3/blob/rawhide/f/gtk3.spec)

* `compiz-cmake-install-path.patch` Compiz installs some cmake files in the wrong directory and this means that Unity can't find them while building. This patch is to be applied with the [compiz9.spec](https://github.com/cat-master21/unityDE-specs/blob/main/compiz9.spec) `Source0`

* `nux-m4.tar.gz` A archive for unityx specific nux which has m4 macros missing. This source is for [nux.spec](https://github.com/cat-master21/unityDE-specs/blob/main/nux-devel.spec)