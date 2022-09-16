Name:           frame-devel
Version:        2.5.0
Release:        1
Summary:        Touch Frame Library
BuildArch:      %{_arch}

License:        GPLv3+
URL:            https://launchpad.net/frame
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/f/frame/frame_2.5.0daily13.06.05+16.10.20160809.orig.tar.gz
Patch0:         http://archive.ubuntu.com/ubuntu/pool/universe/f/frame/frame_2.5.0daily13.06.05+16.10.20160809-0ubuntu3.diff.gz

BuildRequires: automake libtool gnome-common
BuildRequires: intltool
BuildRequires: make
BuildRequires: gcc
BuildRequires: g++
BuildRequires: libX11-devel

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

%files -f files.txt
%doc COPYING COPYING.GPL3

%changelog
