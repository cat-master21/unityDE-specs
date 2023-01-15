Name:           grail-devel
Version:        3.1.1
Release:        1
Summary:        Gesture Recognition And Instantiation Library

License:        GPLv3+
URL:            https://launchpad.net/grail
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/g/grail/grail_3.1.1.orig.tar.bz2

BuildRequires: automake libtool gnome-common
BuildRequires: intltool
BuildRequires: make
BuildRequires: gcc
BuildRequires: g++
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXext-devel
BuildRequires: xorg-x11-server-devel
Requires:      frame-devel

%description
Grail consists of an interface and tools for handling gesture recognition and gesture instantiation.

When a multitouch gesture is performed on a device, the recognizer emits one or several possible gestures. Once the context of the gesture is known, i.e., in what window the touches land and what gestures the clients of that window listen to, the instantiator delivers the matching set of gestures.

The library handles tentative getures, i.e., buffering of events for several alternative gestures until a match is confirmed.

%prep
%setup -q -n grail-%{version}

%build
autoreconf --force --install
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
find . ! -type d -exec ls {} + > %{_builddir}/grail-%{version}/files.txt
popd

sed -i s/^\.\\/// ./files.txt
sed -i 'sn^n%{_usr}/n' ./files.txt
sed -i 's/\.1$/.1.gz/' ./files.txt

%files -f files.txt
%license COPYING COPYING.GPL3

%changelog
%autochangelog
