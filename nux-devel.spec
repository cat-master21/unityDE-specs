Name:           nux-devel
Version:        4.0.8
Release:        1
Summary:        An OpenGL toolkit

License:        GPLv3+ AND LGPLv3+ AND LGPLv2+
URL:            https://gitlab.com/ubuntu-unity/unity-x/nux
Source0:        %{url}/-/archive/main/nux-main.tar.gz
Source1:        https://raw.githubusercontent.com/cat-master21/unityDE-specs/unityx/patches/nux-m4.tar.gz
#Patch0:         http://archive.ubuntu.com/ubuntu/pool/universe/n/nux/nux_4.0.8+18.10.20180623-0ubuntu4.diff.gz
%global source_date_epoch_from_changelog 0

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
Requires:      glib2
Requires:      pciutils
Requires:      libXdamage
Requires:      libXcomposite
Requires:      glewmx-devel
Requires:      pcre
Requires:      libXinerama
Requires:      libXxf86vm
Requires:      glew
Requires:      mesa-libGLU
Requires:      libglvnd
Requires:      libpng
Requires:      libXext
Requires:      libX11
Requires:      libsigc++20
Requires:      cairo
Requires:      pango
Requires:      ibus
Requires:      geis-devel

%description
Visual rendering toolkit for real-time applications.

%prep
%setup -q -n nux-main
# Add missing m4 macros for docs
tar -xf '%{SOURCE1}'
#patch0 -p1
#for i in debian/patches/*.patch; do patch -p1 < $i; done
# Properly find doxygen-include.am
sed -i 's!doxygen-include.am!$(top_srcdir)/doxygen-include.am!' ./Makefile.am

# This subdir fails because it requires glew
#sed -i 's/examples//' Makefile.am

# Why is there a binary files here?
# This is extremelyy problematic
rm ./*/*.o

%build
NOCONFIGURE=1 \
./autogen.sh

PYTHON=%{__python3}
export PYTHON

%configure \
  --enable-documentation=no --enable-opengles-20 \
  --disable-silent-rules \
  --disable-static

%make_build

%install
%make_install
rm -fv %{buildroot}%{_libdir}/*.la %{buildroot}%{python3_sitearch}/*.la

pushd %{buildroot}/usr
find . ! -type d -exec ls {} + > %{_builddir}/%{name}-main/files.txt
popd

sed -i s/^\.\\/// ./files.txt
sed -i 'sn^n%{_usr}/n' ./files.txt
sed -i 's/\.1$/.1.gz/' ./files.txt

%files -f files.txt
%license COPYING COPYING.gpl COPYING.lgpl-v2.1

%changelog
