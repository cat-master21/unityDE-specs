%global source_date_epoch_from_changelog 0

Name:           unity-settings-daemon-devel
Version:        15.04.1+21.10.20220802
#Uses Ubuntu's version as it is maintianed
Release:        1
Summary:        Daemon handling the Unity session settings

License:        GPLv2 AND LGPLv2+
URL:            https://launchpad.net/unity-settings-daemon
Source0:        http://archive.ubuntu.com/ubuntu/pool/universe/u/unity-settings-daemon/unity-settings-daemon_%{version}.orig.tar.gz
Patch0:         http://archive.ubuntu.com/ubuntu/pool/universe/u/unity-settings-daemon/unity-settings-daemon_%{version}-0ubuntu1.diff.gz

BuildRequires: automake libtool gnome-common
BuildRequires: intltool
BuildRequires: make
BuildRequires: gcc
BuildRequires: g++
BuildRequires: glib2-devel
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: lcms2-devel
BuildRequires: libnotify-devel
BuildRequires: libgudev-devel
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXext-devel
BuildRequires: xorg-x11-server-devel
BuildRequires: gperf
BuildRequires: ibus-devel
BuildRequires: accountsservice-devel
BuildRequires: libxkbfile-devel
BuildRequires: xkeyboard-config-devel
BuildRequires: fcitx-devel
BuildRequires: gnome-desktop3-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libcanberra-devel
BuildRequires: alsa-lib-devel
BuildRequires: libXrandr-devel
BuildRequires: upower-devel
BuildRequires: colord-devel
BuildRequires: libwacom-devel
BuildRequires: xorg-x11-drv-wacom-devel
BuildRequires: librsvg2-devel
BuildRequires: libXtst-devel
BuildRequires: PackageKit-glib-devel
BuildRequires: NetworkManager-libnm-devel
Requires:      NetworkManager-libnm
Requires:      PackageKit-glib
Requires:      libXtst
Requires:      librsvg2
Requires:      xorg-x11-drv-wacom
Requires:      libwacom
Requires:      colord
Requires:      upower
Requires:      libXrandr
Requires:      alsa-lib
Requires:      libcanberra
Requires:      pulseaudio-libs
Requires:      gnome-desktop3
Requires:      fcitx-libs
Requires:      xkeyboard-config
Requires:      libxkbfile
Requires:      accountsservice
Requires:      libgudev
Requires:      libnotify
Requires:      gperf
Requires:      lcms2
Requires:      gsettings-ubuntu-touch-schemas-devel
Requires:      gsettings-desktop-schemas

%description
The settings daemon used in Unity 7. It is based on GNOME Settings Daemon 3.8.6.1.

%prep
%setup -q -n unity-settings-daemon-%{version}
%patch0 -p1

%build
export LDFLAGS='-Wl,-O1 -Wl,-z,defs -Wl,--warn-unresolved-symbols -Wl,--as-needed'

NOCONFIGURE=1 \
./autogen.sh

%configure --disable-static --enable-packagekit --enable-ibus --enable-fcitx --enable-network-manager

%make_build


%install
%make_install
rm -fv %{buildroot}%{_libdir}/unity-settings-daemon-1.0/*.la %{buildroot}%{_libdir}/*.la


pushd %{buildroot}
ln -s usr/libexec/unity-settings-daemon usr/bin/unity-settings-daemon
find . ! -type d -exec ls {} + > %{_builddir}/unity-settings-daemon-%{version}/files.txt
popd

sed -i 's/^.//' ./files.txt
sed -i 's/\.1$/.1.gz/' ./files.txt
sed -i 's/libunity-settings-daemon.so.1.gz$/libunity-settings-daemon.so.1/' ./files.txt


%files -f files.txt
%license COPYING COPYING.LIB


%changelog

