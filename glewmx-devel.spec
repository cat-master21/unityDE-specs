Name:           glewmx-devel
Version:        1.13.0
Release:        1
Summary:        OpenGL Extension Wrangler MX
BuildArch:      %{_arch}

License:        GPLv3+
URL:            https://launchpad.net/ubuntu/+source/glewmx
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/g/glewmx/glewmx_%{version}.orig.tar.gz
Source1:        http://archive.ubuntu.com/ubuntu/pool/universe/g/glewmx/glewmx_%{version}-5.debian.tar.xz
%global source_date_epoch_from_changelog 0

BuildRequires: make
BuildRequires: gcc
BuildRequires: mesa-libGLU
BuildRequires: libXmu-devel
BuildRequires: libXi-devel
Requires:      libXi
Requires:      mesa-libGLU
Requires:      libXmu

%description
OpenGL Extension Wrangler MX. The MX version is discountinued but is maintained in Ubuntu.

%prep
%setup -q -n glew-%{version}
tar -x -I 'xz -d -T0 -k' -f '%{SOURCE1}'

for i in debian/patches/*.patch; do patch -p1 < $i; done
sed -i 's:$(GLEW_DEST)/include/GL:$(GLEW_DEST)/include/glewmx-%{version}/GL:' Makefile

%build

%make_build

%install
sed -i 's:includedir=${prefix}/include:includedir=${prefix}/include/glewmx-%{version}:' glewmx.pc
%make_build DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p" install.lib.mx install.mx install.pkgconfig.mx
rm -fv %{buildroot}%{_libdir}/*.a

pushd %{buildroot}/usr
find . ! -type d -exec ls {} + > %{_builddir}/glew-%{version}/files.txt
popd

sed -i s/^\.\\/// ./files.txt
sed -i 'sn^n%{_usr}/n' ./files.txt

%files -f files.txt
%license LICENSE.txt

%changelog
