%define _ubuntu_rel 0ubuntu3

Name:    unity-asset-pool
Summary: Assets for Unity 7
Version: 0.8.24+17.10.20170507
Release: 1

License: GPLv2
URL:     https://packages.ubuntu.com/jammy/unity-asset-pool
Source0: http://archive.ubuntu.com/ubuntu/pool/universe/u/unity-asset-pool/unity-asset-pool_%{version}-%{_ubuntu_rel}_all.deb
BuildArch:	noarch

BuildRequires: binutils
BuildRequires: zstd
Requires:      adwaita-icon-theme
Requires:      hicolor-icon-theme

%description
Theme and icons for Unity 7.

%prep
%setup -q -T -c

%build
ar x %{SOURCE0}
tar --xz -xvf data.tar.xz ./usr/share/doc/unity-asset-pool/copyright
mv -f usr/share/doc/unity-asset-pool/copyright ./COPYING
rm -rf usr

%install
tar --xz -xvf data.tar.xz -C %{buildroot}
rm -rf %{buildroot}/usr/share/doc

pushd %{buildroot}
find . ! -type d -exec ls {} + > %{_builddir}/%{name}-%{version}/files.txt
popd
sed -i 'sX^./X/X' ./files.txt

%files -f files.txt
%license COPYING

%changelog
%autochangelog
