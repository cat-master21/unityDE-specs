Name:           geis-devel
Version:        2.2.17
Release:        1
Summary:        An implementation of the GEIS interface

License:        GPLv3 AND LGPLv3
URL:            https://launchpad.net/geis
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/g/geis/geis_2.2.17+16.04.20160126.orig.tar.gz
Patch0:         http://archive.ubuntu.com/ubuntu/pool/universe/g/geis/geis_2.2.17+16.04.20160126-0ubuntu8.diff.gz
%global source_date_epoch_from_changelog 0

BuildRequires: automake libtool gnome-common
BuildRequires: intltool
BuildRequires: make
BuildRequires: gcc
BuildRequires: g++
BuildRequires: dbus-devel
BuildRequires: python3-devel
Requires:      python3
Requires:      grail-devel
Requires:      frame-devel

%description
An implementation of the GEIS (Gesture Engine Interface and Support) interface.

%prep
%setup -q -n geis-%{version}+16.04.20160126
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
rm -fv %{buildroot}%{_libdir}/*.la %{buildroot}%{python3_sitearch}/*.la

pushd %{buildroot}/usr
find . ! -type d -exec ls {} + > %{_builddir}/geis-%{version}+16.04.20160126/files.txt
popd

sed -i s/^\.\\/// ./files.txt
sed -i 'sn^n%{_usr}/n' ./files.txt
sed -i 's/\.1$/.1.gz/' ./files.txt
sed -i 's/libgeis.so.1.gz$/libgeis.so.1/' ./files.txt

%files -f files.txt
%license COPYING COPYING.GPL

%changelog
