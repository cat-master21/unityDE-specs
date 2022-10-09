%global source_date_epoch_from_changelog 0
%define _ubuntu_rel 1ubuntu4

Name:    unity-session
Summary: Lightdm profile for Unity 7
Version: 42.0
Release: 1

License: GPLv2
URL:     https://packages.ubuntu.com/jammy/unity-session
Source0: http://archive.ubuntu.com/ubuntu/pool/universe/g/gnome-session/unity-session_%{version}-%{_ubuntu_rel}_all.deb
BuildArch:	noarch

BuildRequires: binutils
BuildRequires: zstd
Requires:      unity-shell
Requires:      unity-settings-daemon-devel
Recommends:    lightdm

%description
Autostart and profile for Unity 7 in Lightdm.


%prep
%setup -q -T -c


%build
ar x %{SOURCE0}
tar --zstd -xvf data.tar.zst ./usr/share/doc/unity-session/copyright
mv -f usr/share/doc/unity-session/copyright ./COPYING
rm -rf usr


%install
tar --zstd -xvf data.tar.zst -C %{buildroot}
rm -rf %{buildroot}/usr/share/doc

pushd %{buildroot}
find . ! -type d -exec ls {} + > %{_builddir}/%{name}-%{version}/files.txt
popd
sed -i 'sX^./X/X' ./files.txt


%files -f files.txt
%license COPYING


%changelog

