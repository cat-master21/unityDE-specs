Name:           libunity-misc-devel
Version:        1.4
Release:        1
Summary:        Misc Unity shell libs
BuildArch:      %{_arch}

License:        LGPLv2+
URL:            https://launchpad.net/libunity-misc
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/libu/libunity-misc/libunity-misc_4.0.5+14.04.20140115.orig.tar.gz
# you can't download launchpad bzr sources

BuildRequires:  make
BuildRequires:  g++
BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  gnome-common
BuildRequires:  gtk-doc
BuildRequires:  libX11-devel
BuildRequires:  gtk3-devel
BuildRequires:  glib2-devel
Requires:       gtk3
Requires:       libX11

%description
A simple library that implements a subset of the XPath spec to allow selecting nodes in an object tree

%prep
%setup -q -n libunity-misc-4.0.5+14.04.20140115
find ./ -type f -exec sed -i 's/-Werror//' {} \;
./autogen.sh

%build
$configure
%make_build

%install
%make_install
#This not following prefix that configure makes things more difficult
rm -rf %{buildroot}/src %{buildroot}/lib
mv %{buildroot}/usr/local/* %{buildroot}/usr
rm -rf %{buildroot}/usr/local
mkdir -p %{buildroot}%{_libdir}
cp -r %{buildroot}/usr/lib/* %{buildroot}%{_libdir}/
rm -rf %{buildroot}/usr/lib %{buildroot}%{_libdir}/libunity-misc.la %{buildroot}%{_libdir}/pkgconfig/unity-misc.pc
echo 'prefix=/usr
exec_prefix=${prefix}
libdir=${exec_prefix}/lib64
includedir=${prefix}/include

Name: libunity-misc
Description: A library to build misc for Unity
Version: 4.0.4
Libs: -L${libdir} -lunity-misc
Cflags: -I${includedir}/unity-misc/unity-misc
Requires: glib-2.0 gthread-2.0 gobject-2.0 gio-2.0 gio-unix-2.0 gtk+-3.0' > %{buildroot}%{_libdir}/pkgconfig/unity-misc.pc

%files
%{_libdir}/libunity-misc.so
%{_libdir}/libunity-misc.so.4
%{_libdir}/libunity-misc.so.4.1.0
%{_libdir}/pkgconfig/unity-misc.pc
%{_includedir}/unity-misc/unity-misc/na-tray.h
%{_includedir}/unity-misc/unity-misc/na-marshal.h
%{_includedir}/unity-misc/unity-misc/na-tray-manager.h
%{_includedir}/unity-misc/unity-misc/na-tray-child.h
%{_includedir}/unity-misc/unity-misc/gnome-bg-slideshow.h

%changelog
