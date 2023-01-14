%global source_date_epoch_from_changelog 0
%define __python /usr/bin/python3

Name:           unity-shell
Version:        1.7.6
Release:        1
Summary:        Unity7 is a shell that sings

License:        GPLv3+
URL:            https://gitlab.com/ubuntu-unity/unity-x/unityx
Source0:        %{url}/-/archive/main/unityx-main.tar.gz

BuildRequires: cmake
BuildRequires: g++
BuildRequires: gcc
BuildRequires: dee-devel
BuildRequires: gnome-desktop3-devel
BuildRequires: zeitgeist-devel
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
BuildRequires: chrpath
BuildRequires: systemd-rpm-macros
#Requires:	   unity-data
#Requires:     unity-core
Requires:      pam
Requires:      libunity-misc-devel
Requires:      nux-devel
Requires:      geis-devel
Requires:      unity-settings-daemon-devel
Requires:      libsigc++20
Requires:      bamf
Requires:      libnotify
Requires:      gtk3
Requires:      libstdc++
Requires:      xpathselect-devel
Requires:      libappstream-glib
Requires:      zeitgeist
Requires:      libunity
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
Group:		User Interface/Desktops

# For /usr/etc/pam.d/unity
Recommends: gnome-keyring-pam
Requires:	%{name}%{?_isa} = %{version}-%{release}

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
%setup -q -n unityx-main

%build
%cmake -DUNITY_PROTOCOL_PRIVATE_LIB=%{_libdir}/libunity -DCOMPIZ_BUILD_WITH_RPATH=FALSE -DCOMPIZ_PACKAGING_ENABLED=TRUE -DCOMPIZ_PLUGIN_INSTALL_TYPE=package -DUSE_GSETTINGS=TRUE

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

# Upstart init is dead a long time ago and there isn't any package that provides anything to do with it.
rm -rf %{buildroot}%{_datarootdir}/upstart

%find_lang unity

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/compiz/libunityshell.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/compiz/libunitymtgrabhandles.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libunity-core-6.0.so.9.0.0

%py3_shebang_fix $RPM_BUILD_ROOT%{_libdir}/unity

%preun
%gconf_schema_remove compiz-unitymtgrabhandles compiz-unityshell

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
%dir %{_libdir}/compiz/
%{_libdir}/compiz/libunitymtgrabhandles.so
%{_libdir}/compiz/libunityshell.so
%{_mandir}/man1/unity.1.gz
%dir %{_libdir}/unity/
%{_libdir}/unity/compiz-config-profile-setter
%{_libdir}/unity/compiz-profile-selector
%{_libdir}/unity/systemd-prestart-check
%{_libdir}/unity/unity-panel-service
%{_libdir}/unity/unity-active-plugins-safety-check
%{_libdir}/unity/upstart-prestart-check

%files core
%doc AUTHORS ChangeLog HACKING README
%license COPYING COPYING.LGPL
%{_libdir}/libunity-core-6.0.so.9
%{_libdir}/libunity-core-6.0.so.9.0.0


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
%{_libdir}/unity/makebootchart.py
%{_mandir}/man1/unity-panel-service.1.gz
%{_datadir}/ccsm/icons/hicolor/64x64/apps/plugin-unityshell.png
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.unitymtgrabhandles.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.unityshell.gschema.xml
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/icons/
%dir %{_datadir}/unity/themes/
%{_datadir}/unity/icons/dash-widgets.json
%{_datadir}/unity/icons/*.png
%{_datadir}/unity/icons/*.svg
%{_datadir}/unity/icons/searchingthedashlegalnotice.html
%{_datadir}/unity/themes/dash-widgets.json
%dir %{_datadir}/compiz/
%dir %{_datadir}/compiz/unitymtgrabhandles/
%dir %{_datadir}/compiz/unitymtgrabhandles/images/
%{_datadir}/compiz/unitymtgrabhandles.xml
%{_datadir}/compiz/unityshell.xml
%{_datadir}/compiz/unitymtgrabhandles/images/handle-0.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-1.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-2.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-3.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-4.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-5.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-6.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-7.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-8.png
%{_datadir}/gnome-control-center/keybindings/50-unity-launchers.xml
%{_sysconfdir}/pam.d/unity
%dir %{_datarootdir}/compizconfig/
%dir %{_datarootdir}/compizconfig/upgrades/
%{_datarootdir}/compizconfig/upgrades/*.upgrade
%dir %{_sysconfdir}/compizconfig/
%{_sysconfdir}/compizconfig/unity-lowgfx.ini
%{_sysconfdir}/compizconfig/unity.conf
%{_sysconfdir}/compizconfig/unity.ini
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

