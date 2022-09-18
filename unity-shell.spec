Name:           unity-shell
Version:        0.0.1
Release:        1
Summary:        Unity7 is a shell that sings for the GNOME desktop environment

License:        GPLv3+
URL:            https://gitlab.com/ubuntu-unity/unity/unity
Source0:        %{url}/-/archive/master/unity-master.tar.gz

BuildRequires: cmake
BuildRequires: g++
BuildRequires: gcc
BuildRequires: dee-devel
BuildRequires: gnome-desktop3-devel
BuildRequires: compiz-devel
BuildRequires: zeitgeist-devel
BuildRequires: libappstream-glib-devel
BuildRequires: libdbusmenu-devel
BuildRequires: bamf-devel
BuildRequires: libindicator-gtk3-devel
BuildRequires: json-glib-devel
BuildRequires: libnotify-devel
BuildRequires: libsigc++20-devel
BuildRequires: libunity-devel
Requires:      libunity-misc-devel
#Requires:      nux-devel
#Requires:      libgeis-devel
#Requires:      libunity-settings-daemon-devel
Requires:      libsigc++20
Requires:      bamf
Requires:      libnotify
Requires:      gtk3
Requires:      libstdc++
Requires:      xpathselect-devel
Requires:      libappstream-glib
Requires:      zeitgeist
Requires:      libunity
Requires:      unity-gtk-module-common
Requires:      compiz9
Requires:      libindicator-gtk3

%description
Unity7 is a shell that sings. It is a shell for the GNOME desktop environment.

%prep
%setup -q -n unity-master

%build
%cmake
%cmake_build

%install
%cmake_install

%files

%changelog
