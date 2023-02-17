%define _ubuntu_rel 22.10.20220822-0ubuntu1

Name:           compiz9
Version:        0.9.14.2
Release:        1%{?dist}
Summary:        OpenGL window and compositing manager 0.9.X.X series

License:        GPLv2+ AND LGPLv2+ AND MIT
URL:            https://launchpad.net/compiz
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/c/compiz/compiz_%{version}+%{_ubuntu_rel}.tar.xz
Patch0:         https://raw.githubusercontent.com/cat-master21/unityDE-specs/main/patches/compiz-cmake-install-path.patch

Conflicts:     compiz
BuildRequires: libX11-devel
BuildRequires: libdrm-devel
BuildRequires: libXcursor-devel
BuildRequires: libXfixes-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: libSM-devel
BuildRequires: libICE-devel
BuildRequires: libXmu-devel
BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: librsvg2-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: fuse-devel
BuildRequires: cairo-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libxslt-devel
BuildRequires: glib2-devel
BuildRequires: libwnck3-devel
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: g++
BuildRequires: make
BuildRequires: glibmm24-devel
BuildRequires: lcov
BuildRequires: python3-devel
BuildRequires: boost-devel
BuildRequires: libnotify-devel
BuildRequires: python3-Cython
BuildRequires: glibc-headers-x86
BuildRequires: metacity-devel
BuildRequires: libglvnd-devel
BuildRequires: gcovr
BuildRequires: mesa-libEGL-devel
BuildRequires: glib2-devel
BuildRequires: xorg-x11-server-devel
Requires:      glib2
Requires:      xorg-x11-server-Xorg
Requires:      metacity
Requires:      glx-utils

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for %{name}.

%package -n python3-ccsm
Summary: Compiz Config Manager
Conflicts: ccsm
Requires: %{name}%{?_isa}

%description -n python3-ccsm
Compiz Config Manager helps configure Compiz Window Manager, version 0.9 series

%description
Compiz 9 branch, which is newer then what Fedora packages and required by Unity 7.6 and higher.

%prep
%autosetup -p1 -n compiz

%build
# The driver blacklist hack is obselete
sed -i 's/(nouveau|Intel).*Mesa 8.0//' plugins/opengl/opengl.xml.in
%cmake -DCOMPIZ_DISABLE_GS_SCHEMAS_INSTALL=OFF -DBUILD_GTK=ON -DBUILD_METACITY=ON -DCOMPIZ_BUILD_TESTING=OFF -DBUILD_GLES=ON -DCOMPIZ_PACKAGING_ENABLED=TRUE -DBUILD_XORG_GTEST=OFF -DCOMPIZ_BUILD_WITH_RPATH=FALSE -DCOMPIZ_WERROR=OFF
%cmake_build

%install
%cmake_install

desktop-file-install                              \
    --delete-original                             \
    --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/*.desktop

find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang ccsm
%find_lang compiz

%py3_shebang_fix $RPM_BUILD_ROOT%{_bindir}/ccsm

# placeholder for local icons
mkdir -p %{buildroot}%{_datadir}/compiz/icons/hicolor/{scalable/{apps,\
categories},22x22/{categories,devices,mimetypes}}

%files -f compiz.lang
%doc AUTHORS README INSTALL NEWS
%license COPYING COPYING.GPL COPYING.LGPL COPYING.MIT
%config %{_sysconfdir}/compizconfig/config.conf
%{_bindir}/compiz
%{_bindir}/compiz-decorator
%{_bindir}/gtk-window-decorator
%{_libdir}/libcompizconfig.so.*
%{_libdir}/libcompizconfig_gsettings_backend.so
%{_libdir}/libcompiz_core.so.*
%{_libdir}/libdecoration.so.*
%dir %{_libdir}/compiz
%{_libdir}/compiz/*.so
%dir %{_libdir}/compizconfig
%dir %{_libdir}/compizconfig/backends
%{_libdir}/compizconfig/backends/*.so
%{python3_sitearch}/compizconfig.cpython*.so
%{python3_sitearch}/compizconfig_python*.egg-info/
%{_datadir}/applications/compiz.desktop
#{_datadir}/compiz/
%{_datadir}/glib-2.0/schemas/org.compiz*.gschema.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-*.xml

%files devel
%{_includedir}/compiz/
%dir %{_includedir}/compizconfig
%{_includedir}/compizconfig/*.h
%{_libdir}/libcompizconfig.so
%{_libdir}/libcompiz_core.so
%{_libdir}/libdecoration.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/cmake/Modules/*.cmake

%files -n python3-ccsm -f ccsm.lang
%doc AUTHORS NEWS
%license COPYING
%{_bindir}/ccsm
%{_datadir}/applications/ccsm.desktop
%dir %{_datadir}/ccsm
%{_datadir}/ccsm/*
%{_datadir}/icons/hicolor/*/apps/ccsm.png
%{_datadir}/icons/hicolor/*/apps/ccsm.svg
%dir %{python3_sitelib}/ccm
%{python3_sitelib}/ccm/*
%{python3_sitelib}/ccsm-%{version}-py%{python3_version}.egg-info

%changelog
%autochangelog
