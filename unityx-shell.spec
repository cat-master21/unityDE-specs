# Spectool has a bug where it can't download from https://gitlab.com/ubuntu-unity/unity-x/unityx
%global forgeurl https://gitlab.com/cat-master21/unityx
%global commit a43578fa78f12ff47bb4d7d88d373333cd4af532
%forgemeta

%define __python /usr/bin/python3

Name:          unityx-shell
Version:       1.7.7
Release:       1%{?dist}
Summary:       Unity7 is a shell that sings

License:       GPLv3 AND LGPLv3
URL:           %{forgeurl}
Source0:       %{forgesource}
Source1:       https://gitlab.xfce.org/panel-plugins/xfce4-windowck-plugin/-/raw/eeffa180d4b0828bcd4e9da0c504ac6524e1a0b4/configure.ac.in
Source2:       https://gitlab.xfce.org/panel-plugins/xfce4-windowck-plugin/-/commit/dee596492f006d02e2b39abd072ddd7b37fefe82.diff
Source3:       https://git.launchpad.net/compiz/plain/compizconfig/gsettings/org.compiz.gschema.xml

Provides:      unity-shell
BuildRequires: cmake
BuildRequires: g++
BuildRequires: gcc
BuildRequires: pkgconfig(dee-1.0)
BuildRequires: pkgconfig(unity-settings-daemon)
BuildRequires: pkgconfig(gnome-desktop-3.0)
BuildRequires: zeitgeist-devel
BuildRequires: libappstream-glib-devel
BuildRequires: libdbusmenu-devel
BuildRequires: bamf-devel
BuildRequires: libindicator-gtk3-devel
BuildRequires: json-glib-devel
BuildRequires: libnotify-devel
BuildRequires: libsigc++20-devel
#BuildRequires: xpathselect-devel
#BuildRequires: libunity-devel
BuildRequires: doxygen
BuildRequires: pam-devel
BuildRequires: boost-devel
BuildRequires: pkgconfig(nux-4.0)
BuildRequires: gtk3-devel
BuildRequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(unity-protocol-private)

# unityx-shell-xfce4-windowck-plugin
BuildRequires: pkgconfig(libwnck-3.0)
BuildRequires: pkgconfig(libxfconf-0)
BuildRequires: pkgconfig(libxfce4util-1.0)
BuildRequires: pkgconfig(libxfce4ui-2)
BuildRequires: pkgconfig(libxfce4panel-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: xfce4-vala
BuildRequires: xfce4-dev-tools

Requires:      python3-pydbus
Requires:      python3-psutil
Requires:      unity-asset-pool
Requires:      libunity-misc-devel
Requires:      geis-devel
Requires:      unity-settings-daemon
Requires:      unity-gtk3-module
Requires:      unity-gtk2-module
Requires:      libindicator-gtk3
Requires:      plotinus%{?_isa} = %{version}-%{release}
Requires:      bamf-daemon
Requires:      xbindkeys
# For default configuration
Requires:      %{name}-xfce4-windowck-plugin%{?_isa} = %{version}-%{release}
Requires:      nemo
Requires:      blueman
Requires:      network-manager-applet
Requires:      xfce4-vala-panel-appmenu-plugin
Requires:      xfwm4

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


%package xfce4-windowck-plugin
Summary:	Core library for the Unity shell

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description xfce4-windowck-plugin
This package contains the core library needed for Unity and Unity 2D.


%package devel
Summary:	Development files for the core Unity library

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(dee-1.0)
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(sigc++-2.0)
Requires:	pkgconfig(unity)
Requires:	pkgconfig(nux-4.0)

%description devel
This package contains the development files the core Unity library.


%package -n plotinus
Summary:	Automatic testing for Unity
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n plotinus
This package contains the autopilot framework, which allows for triggering
keyboard and mouse events automatically. This package also contains the bindings
needed for writing automated tests in Python.

%prep
%forgeautosetup

%build
# Wrong paths
sed -i 's!lib/{arch}-linux-gnu!%{_lib}!' unityx/unityx
sed -i 's!%{_lib}/bamf/bamfdaemon!libexec/bamf/bamfdaemon!' unityx/unityx
sed -i 's!unity-settings-daemon!%{_libexecdir}/unity-settings-daemon!' unityx/unityx
%py3_shebang_fix unityx/unityx

# Fix invalid argument calling dbus-update-activation-environment
sed -i 's/'--all', //' unityx/unityx

# Remove rpath
sed -i '/RPATH/d' UnityCore/CMakeLists.txt
sed -i 's/SOVERSION ${CORE_LIB_LT_CURRENT}/SOVERSION ${CORE_LIB_LT_CURRENT})/' UnityCore/CMakeLists.txt

# The caches again!!
rm -fv unityx/windowck-plugin/po/.intltool-merge-cache*

%cmake -DENABLE_X_SUPPORT=ON
%cmake_build

pushd unityx/plotinus
# Wrong path again
sed -i 's/LIBRARY DESTINATION lib/LIBRARY DESTINATION %{_lib}/' CMakeLists.txt
%cmake
%cmake_build
popd

pushd unityx/windowck-plugin
cp %{SOURCE1} configure.ac.in
# Fix the file missing and icons being blurry
patch -i %{SOURCE2} -p1

NOCONFIGURE=1 \
./autogen.sh

%configure --disable-static
%make_build
popd

%install
%cmake_install

pushd unityx/plotinus
%cmake_install
popd

pushd unityx/windowck-plugin
%make_install
rm -fv %{buildroot}%{_libdir}/*.la
popd

# unityx-launcher still requires compiz gsettings schema and the 8 series doesn't provide one
# Though it isn't really needed aside from that
install -m 0644 %{SOURCE3} -t %{buildroot}%{_datarootdir}/glib-2.0/schemas

%find_lang unityx
%find_lang xfce4-windowck-plugin

%preun

%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files -f unityx.lang
%doc AUTHORS ChangeLog INSTALL README.md
%license COPYING COPYING.LGPL
%{_bindir}/unityx*
%{_libdir}/libunityx-core-6.0.so.*
%{_datadir}/glib-2.0/schemas/org.unityd.UnityX.gschema.xml
%{_datadir}/glib-2.0/schemas/org.unityd.UnityX.user-interface.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.gschema.xml
%dir %{_datadir}/unityx
%dir %{_datadir}/unityx/icons
%{_datadir}/unityx/icons/dash-widgets.json
%{_datadir}/unityx/icons/*.png
%{_datadir}/unityx/icons/*.svg
%{_datadir}/unityx/icons/searchingthedashlegalnotice.html
%dir %{_datadir}/unityx/themes/
%{_datadir}/unityx/themes/dash-widgets.json
%{_datadir}/xsessions/unityx.desktop

%files -n plotinus
%doc unityx/plotinus/README.md
%license COPYING COPYING.LGPL
%{_bindir}/plotinus
%{_libdir}/libplotinus.so
%{_datadir}/glib-2.0/schemas/org.unityd.UnityX.plotinus.gschema.xml

%files devel
%dir %{_includedir}/UnityX-6.0/UnityCore/
%{_includedir}/UnityX-6.0/UnityCore/*.h
%{_libdir}/libunityx-core-6.0.so
%{_libdir}/pkgconfig/unityx-core-6.0.pc


%files xfce4-windowck-plugin -f xfce4-windowck-plugin.lang
%doc unityx/windowck-plugin/AUTHORS unityx/windowck-plugin/NEWS unityx/windowck-plugin/README.md
%license unityx/windowck-plugin/COPYING
%{_libdir}/xfce4/panel/plugins/*.so
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/themes/Windowck/
%{_datadir}/themes/Windowck-dark/
%{_datadir}/xfce4/panel/plugins/*.desktop

%changelog
%autochangelog
