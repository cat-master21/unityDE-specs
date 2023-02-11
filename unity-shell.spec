%global forgeurl https://gitlab.com/ubuntu-unity/unity/unity
%global commit f2fb4437821b083a655e82c6fc97cb9d04c70041
%forgemeta

Name:           unity-shell
Version:        1.7.7
Release:        1%{?dist}
Summary:        Unity is a shell that sings

License:        GPLv3+
# forgeurl doesn't really work with spectool, tries https://gitlab.com/ubuntu-unity/unity instead of https://gitlab.com/ubuntu-unity/unity/unity
URL:            https://gitlab.com/ubuntu-unity/unity/unity
Source0:        %{url}/-/archive/%commit/unity-%commit.tar.bz2
Patch0:         0001-Remove-xpathselect-dependency.patch
Patch1:         0002-Remove-ido-dependency.patch
Patch2:         0003-Remove-social-scope.patch

BuildRequires: cmake
BuildRequires: g++
BuildRequires: gcc
BuildRequires: dee-devel
BuildRequires: gnome-desktop3-devel
BuildRequires: pkgconfig(zeitgeist-2.0)
BuildRequires: libappstream-glib-devel
BuildRequires: libdbusmenu-devel
BuildRequires: bamf-devel
BuildRequires: libindicator-gtk3-devel
BuildRequires: json-glib-devel
BuildRequires: libnotify-devel
BuildRequires: libsigc++20-devel
BuildRequires: libunity-devel
BuildRequires: doxygen
BuildRequires: pam-devel
BuildRequires: boost-devel
BuildRequires: python3-devel
BuildRequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(nux-4.0)
BuildRequires: compiz9-devel
BuildRequires: pkgconfig(unity-misc)
BuildRequires: chrpath
BuildRequires: systemd-rpm-macros
Requires:      gsettings-ubuntu-touch-schemas
Requires:      unity-scope-home
Requires:      %{name}-data = %{version}-%{release}
Requires:      %{name}-core%{?_isa} = %{version}-%{release}
Requires:      pam
Requires:      libunity-misc-devel
Requires:      geis-devel
Requires:      bamf
Requires:      unity-gtk-module-common
Requires:      compiz9
Requires:      libindicator-gtk3

%description
Unity is a desktop experience that sings. Designed by Canonical and the Ayatana
community, Unity is all about the combination of familiarity and the future. We
bring together visual design, analysis of user experience testing, modern
graphics technologies and a deep understanding of the free software landscape to
produce what we hope will be the lightest, most elegant and most delightful way
to use your PC.

The Unity desktop experience is designed to allow for multiple implementations,
currently, Unity consists of a Compiz plugin based visual interface only, which
is heavily dependent on OpenGL.

%package core
Summary:	Core library for the Unity shell
Group:		System Environment/Libraries
Requires:	%{name}-data = %{version}-%{release}

%description core
This package contains the core library needed for Unity and Unity 2D.

%package core-devel
Summary:	Development files for the core Unity library
Group:		Development/Libraries
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(dee-1.0)
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(sigc++-2.0)
Requires:	pkgconfig(unity)
Requires:	pkgconfig(nux-4.0)

%description core-devel
This package contains the development files the core Unity library.

%package data
Summary:	Common files for the Unity shell
BuildArch:      noarch
Group:		User Interface/Desktops
# For /usr/etc/pam.d/unity
Recommends:     gnome-keyring-pam
Requires:	%{name} = %{version}-%{release}

%description data
This package contains data (non-arch specific) files to Unity 7.

%package autopilot
Summary:	Automatic testing for Unity
Group:		Development/Tools
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}

%description autopilot
This package contains the autopilot framework, which allows for triggering
keyboard and mouse events automatically. This package also contains the bindings
needed for writing automated tests in Python.

%prep
%autosetup -n unity-%commit -p1

%build
%cmake -DUNITY_PROTOCOL_PRIVATE_LIB=%{_libdir}/libunity/libunity-protocol-private.so.0.0.0 -DCOMPIZ_BUILD_WITH_RPATH=FALSE -DCOMPIZ_PACKAGING_ENABLED=TRUE -DCOMPIZ_PLUGIN_INSTALL_TYPE=package -DUSE_GSETTINGS=TRUE -DENABLE_UNIT_TESTS=FALSE

%cmake_build

pushd tests/autopilot/
%py3_build
popd

%install

pushd tests/autopilot/
%py3_install
popd

%cmake_install

# Not the correct directory, /usr/etc/pam.d should be /etc/pam.d
mv -f %{buildroot}%{_prefix}%{_sysconfdir}/* %{buildroot}%{_sysconfdir}
rm -rf %{buildroot}%{_prefix}%{_sysconfdir}
# Upstart init is dead a long time ago and there isn't any package that provides anything to do with it.
rm -rf %{buildroot}%{_datadir}/upstart
# Needed directory for unity-panel-service
mkdir %{buildroot}%{_datadir}/unity/indicators

%find_lang unity

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/compiz/libunityshell.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/compiz/libunitymtgrabhandles.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libunity-core-6.0.so.9.0.0

%py3_shebang_fix $RPM_BUILD_ROOT%{_bindir}/unity
%py3_shebang_fix $RPM_BUILD_ROOT%{_libdir}/unity/makebootchart.py

%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%post core -p /sbin/ldconfig

%postun core -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog HACKING README
%license COPYING COPYING.LGPL
%{_bindir}/unity
%{_libdir}/compiz/libunitymtgrabhandles.so
%{_libdir}/compiz/libunityshell.so
%{_mandir}/man1/unity.1.gz
%{_mandir}/man1/unity-panel-service.1.gz
%dir %{_libdir}/unity/
%{_libdir}/unity/compiz-config-profile-setter
%{_libdir}/unity/compiz-profile-selector
%{_libdir}/unity/systemd-prestart-check
%{_libdir}/unity/makebootchart.py
%{_libdir}/unity/unity-panel-service
%{_libdir}/unity/unity-active-plugins-safety-check
%{_libdir}/unity/upstart-prestart-check

%files core
%doc AUTHORS ChangeLog HACKING README
%license COPYING COPYING.LGPL
%{_libdir}/libunity-core-6.0.so.*

%files core-devel
%doc AUTHORS ChangeLog HACKING README
%license COPYING COPYING.LGPL
%dir %{_includedir}/Unity-6.0/
%dir %{_includedir}/Unity-6.0/UnityCore/
%{_includedir}/Unity-6.0/UnityCore/*.h
%{_libdir}/libunity-core-6.0.so
%{_libdir}/pkgconfig/unity-core-6.0.pc

%files data -f unity.lang
%doc AUTHORS ChangeLog HACKING README
%license COPYING COPYING.LGPL
%{_datadir}/ccsm/icons/hicolor/64x64/apps/plugin-unityshell.png
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.unitymtgrabhandles.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.unityshell.gschema.xml
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/indicators/
%dir %{_datadir}/unity/icons/
%{_datadir}/unity/icons/dash-widgets.json
%{_datadir}/unity/icons/*.png
%{_datadir}/unity/icons/*.svg
%{_datadir}/unity/icons/searchingthedashlegalnotice.html
%dir %{_datadir}/unity/themes/
%{_datadir}/unity/themes/dash-widgets.json
%{_datadir}/compiz/unitymtgrabhandles.xml
%{_datadir}/compiz/unityshell.xml
%dir %{_datadir}/compiz/unitymtgrabhandles
%dir %{_datadir}/compiz/unitymtgrabhandles/images/
%{_datadir}/compiz/unitymtgrabhandles/images/handle-*.png
%{_datadir}/gnome-control-center/keybindings/50-unity-launchers.xml
%{_sysconfdir}/pam.d/unity
%{_datadir}/compizconfig/upgrades/*.upgrade
%{_sysconfdir}/compizconfig/unity*
%{_userunitdir}/unity*.service
%{_userunitdir}/unity*.target

%files autopilot
%doc AUTHORS ChangeLog HACKING README
%license COPYING COPYING.LGPL
%dir %{python3_sitelib}/unity-1.0-py%{python3_version}.egg-info/
%{python3_sitelib}/unity-1.0-py%{python3_version}.egg-info/PKG-INFO
%{python3_sitelib}/unity-1.0-py%{python3_version}.egg-info/SOURCES.txt
%{python3_sitelib}/unity-1.0-py%{python3_version}.egg-info/dependency_links.txt
%{python3_sitelib}/unity-1.0-py%{python3_version}.egg-info/top_level.txt
# Tests
%dir %{python3_sitelib}/unity/
%{python3_sitelib}/unity/__init__.py*
%dir %{python3_sitelib}/unity/emulators/
%{python3_sitelib}/unity/emulators/__init__.py*
%{python3_sitelib}/unity/emulators/dash.py*
%{python3_sitelib}/unity/emulators/X11.py*
%{python3_sitelib}/unity/emulators/compiz.py*
%{python3_sitelib}/unity/emulators/ibus.py
%{python3_sitelib}/unity/emulators/hud.py*
%{python3_sitelib}/unity/emulators/icons.py*
%{python3_sitelib}/unity/emulators/launcher.py*
%{python3_sitelib}/unity/emulators/panel.py*
%{python3_sitelib}/unity/emulators/quicklist.py*
%{python3_sitelib}/unity/emulators/screen.py*
%{python3_sitelib}/unity/emulators/shortcut_hint.py*
%{python3_sitelib}/unity/emulators/switcher.py*
%{python3_sitelib}/unity/emulators/tooltip.py*
%{python3_sitelib}/unity/emulators/unity.py*
%{python3_sitelib}/unity/emulators/window_manager.py*
%{python3_sitelib}/unity/emulators/workspace.py*
%dir %{python3_sitelib}/unity/tests/
%{python3_sitelib}/unity/tests/__init__.py*
%dir %{python3_sitelib}/unity/tests/launcher/
%{python3_sitelib}/unity/tests/launcher/__init__.py*
%{python3_sitelib}/unity/tests/test_gnome_key_grabber.py*
%{python3_sitelib}/unity/tests/test_gobject_introspection.py*
%{python3_sitelib}/unity/tests/test_search.py*
%{python3_sitelib}/unity/tests/test_wm_keybindings.py*
%{python3_sitelib}/unity/tests/launcher/test_capture.py*
%{python3_sitelib}/unity/tests/launcher/test_icon_behavior.py*
%{python3_sitelib}/unity/tests/launcher/test_keynav.py*
%{python3_sitelib}/unity/tests/launcher/test_reveal.py*
%{python3_sitelib}/unity/tests/launcher/test_shortcut.py*
%{python3_sitelib}/unity/tests/launcher/test_switcher.py*
%{python3_sitelib}/unity/tests/launcher/test_visual.py*
%{python3_sitelib}/unity/tests/launcher/test_scroll.py*
%{python3_sitelib}/unity/tests/launcher/test_tooltips.py*
%{python3_sitelib}/unity/tests/test_command_lens.py*
%{python3_sitelib}/unity/tests/test_dash.py*
%{python3_sitelib}/unity/tests/test_home_lens.py*
%{python3_sitelib}/unity/tests/test_hud.py*
%{python3_sitelib}/unity/tests/test_ibus.py*
%{python3_sitelib}/unity/tests/test_panel.py*
%{python3_sitelib}/unity/tests/test_quicklist.py*
%{python3_sitelib}/unity/tests/test_shopping_lens.py*
%{python3_sitelib}/unity/tests/test_shortcut_hint.py*
%{python3_sitelib}/unity/tests/test_showdesktop.py*
%{python3_sitelib}/unity/tests/test_spread.py*
%{python3_sitelib}/unity/tests/test_switcher.py*
%{python3_sitelib}/unity/tests/test_unity_logging.py*
%dir %{python3_sitelib}/unity/tests/xim/
%{python3_sitelib}/unity/tests/xim/__init__.py*
%{python3_sitelib}/unity/tests/xim/test_gcin.py*
%dir %{python3_sitelib}/unity/__pycache__/
%{python3_sitelib}/unity/__pycache__/**
%dir %{python3_sitelib}/unity/emulators/__pycache__/
%{python3_sitelib}/unity/emulators/__pycache__/**
%dir %{python3_sitelib}/unity/tests/__pycache__/
%{python3_sitelib}/unity/tests/__pycache__/**
%dir %{python3_sitelib}/unity/tests/launcher/__pycache__/
%{python3_sitelib}/unity/tests/launcher/__pycache__/**
%dir %{python3_sitelib}/unity/tests/xim/__pycache__/
%{python3_sitelib}/unity/tests/xim/__pycache__/**

%changelog
%autochangelog
