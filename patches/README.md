This Directory contains patches, either modifications to spec files or sources.

* ~~`add-files-to-meson.patch` Ubuntu's patches for gtk3 create new files and applies it's files to autoconfig but not to meson which Fedora uses. This is a patch for `gtk3.spec`~~

* ~~`gtk3-ubuntu.patch` Ubuntu adds files to it's gtk3 (`ubuntu-private.h`, `ubuntumenuitemfactory.h`, etc) and other patches used specifically for Unity and is required for some packages (`ido` for example). This patch should be reapplied every once and awhile. This is a patch for `gtk3 spec`~~

* `compiz-cmake-install-path.patch` Compiz installs some cmake files in the wrong directory and this means that Unity can't find them while building. This patch is to be applied with the `compiz9.spec`

* `nux-m4.tar.gz` A archive for unityx specific nux which has m4 macros missing. This is for `nux.spec`. This may be removed at some point.

* `unity-settings-daemon.service` Is a systemd service that is in a patch but not in archive so (to not rely on patch) adding it here. This is for `unity-settings-daemon.spec`

* `0001-Remove-xpathselect-dependency.patch` This patch removes the unneeded dependency of `xpathselect` from Unity which is extremely old (last commit in 2014). This is for `unity-shell.spec`

* `0001-Remove-social-scope.patch` and `0003-Remove-social-scope.patch` are used to remove the social.scope which is not used anymore. `0001-Remove-social-scope.patch` is used in `unityx-shell.spec` and `0003-Remove-social-scope.patch` is used in `unity-shell.spec`.