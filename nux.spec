Name:           nux
Version:        4.0.8
Release:        1%{?dist}
Summary:        An OpenGL toolkit

License:        GPLv3+ AND LGPLv3+ AND LGPLv2+
URL:            https://gitlab.com/ubuntu-unity/unity-x/nux
Source0:        %{url}/-/archive/main/nux-main.tar.gz
Source1:        https://raw.githubusercontent.com/cat-master21/unityDE-specs/unityx/patches/nux-m4.tar.gz
Patch0:         https://gitlab.com/unity-for-arch/nux/-/raw/main/add_setupframebufferobject_clear.patch

BuildRequires: automake libtool gnome-common
BuildRequires: intltool
BuildRequires: make
BuildRequires: gcc
BuildRequires: g++
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXext-devel
BuildRequires: xorg-x11-server-devel
BuildRequires: libsigc++20-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: cairo-devel
BuildRequires: libpng-devel
BuildRequires: libglvnd-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: glew-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXinerama-devel
BuildRequires: pcre-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: pciutils-devel
BuildRequires: glib2-devel
BuildRequires: ibus-devel
BuildRequires: boost-devel
Requires:      glewmx-devel
Requires:      geis-devel

%description
Visual rendering toolkit for real-time applications.

%package devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%prep
%autosetup -n nux-main -p1
# configure.ac errors without
tar -xf '%{SOURCE1}'
# Properly find doxygen-include.am
sed -i 's!doxygen-include.am!$(top_srcdir)/doxygen-include.am!' ./Makefile.am
# Why are there binary files here?
rm -f ./*/*.o
# Fix path
sed -i 's!/usr/lib!%{_libexecdir}!' debian/50_check_unity_support

%build
NOCONFIGURE=1 \
./autogen.sh

PYTHON=%{__python3}
export PYTHON

%configure \
  --enable-documentation=no \
  --disable-silent-rules \
  --disable-static

%make_build

%install
%make_install
rm -fv %{buildroot}%{_libdir}/*.la %{buildroot}%{python3_sitearch}/*.la
mkdir -p %{buildroot}%{_sysconfdir}/X11/Xsession.d
install -m 0644 debian/50_check_unity_support -t %{buildroot}%{_sysconfdir}/X11/Xsession.d
# Not needed and out of place
rm -rf %{buildroot}%{_datadir}/nux/gputests

%files
%license COPYING COPYING.gpl COPYING.lgpl-v2.1
%{_sysconfdir}/X11/Xsession.d/50_check_unity_support
%{_libdir}/libnux-4.0.so.*
%{_libdir}/libnux-core-4.0.so.*
%{_libdir}/libnux-graphics-4.0.so.*
%dir %{_libexecdir}/nux
%{_libexecdir}/nux/unity_support_test
%dir %{_datadir}/nux
%dir %{_datadir}/nux/4.0
%{_datadir}/nux/4.0/Fonts/
%{_datadir}/nux/4.0/UITextures/

%files devel
%dir %{_includedir}/Nux-4.0
%{_includedir}/Nux-4.0/Nux/
%{_includedir}/Nux-4.0/NuxCore/
%{_includedir}/Nux-4.0/NuxGraphics/
%{_libdir}/libnux-4.0.so
%{_libdir}/libnux-core-4.0.so
%{_libdir}/libnux-graphics-4.0.so
%{_libdir}/pkgconfig/*.pc

%changelog
%autochangelog
