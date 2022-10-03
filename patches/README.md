This Directory contains patches, either modifications to spec files or sources.

* `add-files-to-meson.patch` Ubuntu's patches for gtk3 create new files and applies it's files to autoconfig but not to meson which Fedora uses. This is a patch for [gtk3.spec](https://src.fedoraproject.org/rpms/gtk3/blob/rawhide/f/gtk3.spec)

* `gtk3-ubuntu.patch` Ubuntu adds files to it's gtk3 (`ubuntu-private.h`, `ubuntumenuitemfactory.h`, etc) and other patches used specifically for Unity and is required for some packages (`ido` for example). This patch should be reapplied every once and awhile. This is a patch for [gtk3 spec](https://src.fedoraproject.org/rpms/gtk3/blob/rawhide/f/gtk3.spec) to be patched.

* `libindicator-16.10.0.patch` Fedora uses a outdated version of libindicator which cannot be used for Unity So it must be patched. This is a patch for [libindicator.spec](https://src.fedoraproject.org/rpms/libindicator/blob/rawhide/f/libindicator.spec)
