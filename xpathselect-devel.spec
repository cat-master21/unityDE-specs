Name:           xpathselect-devel
Version:        1.4
Release:        1%{?dist}
Summary:        Implements a subset of the XPath spec

License:        GPLv3+
URL:            https://launchpad.net/xpathselect
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/x/xpathselect/xpathselect_1.4+15.10.20150824.1.orig.tar.gz

BuildRequires:  cmake
BuildRequires:  g++
BuildRequires:  gcc
BuildRequires:  boost-devel
Requires:       libstdc++

%description
A simple library that implements a subset of the XPath spec to allow selecting nodes in an object tree

%prep
%setup -q -n xpathselect-1.4+15.10.20150824.1
sed -i 's/^add_subdirectory(test)//' ./CMakeLists.txt

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%{_libdir}/libxpathselect.so.1.4
%{_libdir}/libxpathselect.so
%{_includedir}/xpathselect/node.h
%{_includedir}/xpathselect/xpathselect.h
%{_libdir}/pkgconfig/xpathselect.pc

%changelog
%autochangelog
