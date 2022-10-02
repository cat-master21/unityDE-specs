This Directory contains patches, either modifications to spec files or patches for sources.

* `add-files-to-meson.patch` Ubuntu only applies it's files to autoconfig but not to meson which Fedora uses.
* `gtk3-ubuntu.patch` Ubuntu adds files to it's gtk3 (`ubuntu-private.h`, `ubuntumenuitemfactory.h`, etc) and other patches used specifically for Unity and is required for some packages (`ido` for example). This patch should be reapplied every once and awhile.
