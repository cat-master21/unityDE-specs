%global source_date_epoch_from_changelog 0
%define _ubuntu_rel 22.10.20220822-0ubuntu1

Name:           compiz9
License:        GPLv2+ AND LGPLv2+ AND MIT
Version:        0.9.14.2
Release:        1
Summary:        OpenGL window and compositing manager 0.9.X.X series
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

%package ccsm9
Summary: Compiz Config Manager
Conflicts: ccsm
Requires: %{name}%{?_isa}

%description ccsm9
Compiz Config Manager helps configure Compiz Window Manager, version 0.9 series

%description
Compiz 9 branch, which is newer then what Fedora packages and required by Unity 7.6 and higher.

%prep
%setup -q -n compiz
%patch0 -p1

%build
%cmake -DCOMPIZ_DISABLE_GS_SCHEMAS_INSTALL=OFF -DBUILD_GTK=On -DBUILD_METACITY=On -DCOMPIZ_BUILD_TESTING=Off -DBUILD_GLES=ON -DCOMPIZ_PACKAGING_ENABLED=TRUE -DBUILD_XORG_GTEST=OFF -DCOMPIZ_BUILD_WITH_RPATH=FALSE -DCOMPIZ_WERROR=Off
%cmake_build

%install
%cmake_install

desktop-file-install                              \
    --delete-original                             \
    --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/*.desktop

find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

%find_lang ccsm

# placeholder for local icons
mkdir -p %{buildroot}%{_datadir}/compiz/icons/hicolor/{scalable/{apps,\
categories},22x22/{categories,devices,mimetypes}}

pushd %{buildroot}/usr
find . ! -type d -exec ls {} + | grep -v ccm | grep -v ccsm | grep -v ccm | grep -v python > %{_builddir}/compiz/files.txt
popd

sed -i s/^\.\\/// ./files.txt
sed -i 'sn^n%{_usr}/n' ./files.txt

%files -f files.txt
%doc AUTHORS README INSTALL NEWS
%license COPYING COPYING.GPL COPYING.LGPL COPYING.MIT
%config %{_sysconfdir}/compizconfig/config.conf

%files ccsm9 -f ccsm.lang
%doc AUTHORS NEWS
%license COPYING
%{_bindir}/ccsm
%{_datadir}/applications/ccsm.desktop
%dir %{_datadir}/ccsm
%{_datadir}/ccsm/*
%{_datadir}/icons/hicolor/*/apps/ccsm.*
%dir %{python3_sitelib}/ccm
%{python3_sitelib}/ccm/*
%{python3_sitelib}/ccsm-%{version}-py%{python3_version}.egg-info
%{python3_sitearch}/*

%changelog

