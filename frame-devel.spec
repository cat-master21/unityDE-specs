Name:           frame-devel
Version:        2.5.0
Release:        1
Summary:        Touch Frame Library

License:        GPLv3+
URL:            https://launchpad.net/frame
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/f/frame/frame_2.5.0daily13.06.05+16.10.20160809.orig.tar.gz
Patch0:         http://archive.ubuntu.com/ubuntu/pool/universe/f/frame/frame_2.5.0daily13.06.05+16.10.20160809-0ubuntu3.diff.gz
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
BuildRequires: asciidoc

%description
Frame handles the buildup and synchronization of a set of simultaneous touches.

%prep
%setup -q -c
%patch0 -p1

%build
NOCONFIGURE=1 \
./autogen.sh

PYTHON=%{__python3}
export PYTHON

%configure \
  --disable-silent-rules \
  --disable-static

%make_build

%install
%make_install
rm -fv %{buildroot}%{_libdir}/*.la

pushd %{buildroot}/usr
find . ! -type d -exec ls {} + > %{_builddir}/frame-devel-%{version}/files.txt
popd

sed -i s/^\.\\/// ./files.txt
sed -i 'sn^n%{_usr}/n' ./files.txt
sed -i 's/frame-test-x11.1/frame-test-x11.1.gz/' ./files.txt

%files -f files.txt
%license COPYING COPYING.GPL3

%changelog
