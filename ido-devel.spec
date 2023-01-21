Name:           ido-devel
Version:        13.10.0
Release:        1%{?dist}
Summary:        Indicators and Display Objects

License:        LGPLv3+ AND LGPLv2+
URL:            https://launchpad.net/ido
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/i/ido/ido_%{version}+17.04.20161028.orig.tar.gz
Patch0:         http://archive.ubuntu.com/ubuntu/pool/universe/i/ido/ido_%{version}+17.04.20161028-0ubuntu3.diff.gz

BuildRequires: automake libtool gnome-common
BuildRequires: intltool
BuildRequires: make
BuildRequires: gcc
BuildRequires: g++
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: asciidoc
BuildRequires: gobject-introspection-devel
BuildRequires: gtk3-devel
BuildRequires: gtest-devel
BuildRequires: gtk-doc
BuildRequires: vala
Requires:      gobject-introspection
Requires:      libX11
Requires:      gtk3

%description
Widgets and other objects used for indicators.

%prep
%setup -q -c
%patch0 -p1

%build
sed -i 's/tests//' ./Makefile.am
sed -i '149d' ./configure.ac
sed -i 's.-Wno-error=deprecated-declarations..' ./src/Makefile.am
NOCONFIGURE=1 \
./autogen.sh

#sed -i '48d' ./tests/Makefile.am

%configure \
  --disable-silent-rules \
  --disable-static

%make_build

%install
%make_install
rm -fv %{buildroot}%{_libdir}/*.la

pushd %{buildroot}/usr
find . ! -type d -exec ls {} + > %{_builddir}/ido-devel-%{version}/files.txt
popd

sed -i s/^\.\\/// ./files.txt
sed -i 'sn^n%{_usr}/n' ./files.txt

%files -f files.txt
%license COPYING COPYING.LGPL.2.1

%changelog
%autochangelog
