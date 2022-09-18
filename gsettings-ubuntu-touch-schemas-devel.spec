Name:           gsettings-ubuntu-touch-schemas-devel
Version:        0.0.7+21.10.20210712
Release:        1
Summary:        Shared GSettings schemas for Ubuntu touch settings

License:        GPLv2 AND LGPLv2.1
URL:            https://launchpad.net/gsettings-ubuntu-touch-schemas
Source0:        http://archive.ubuntu.com/ubuntu/pool/main/g/gsettings-ubuntu-touch-schemas/gsettings-ubuntu-touch-schemas_%{version}.orig.tar.gz
%global source_date_epoch_from_changelog 0

BuildRequires: automake libtool gnome-common
BuildRequires: intltool
BuildRequires: make
BuildRequires: gcc
BuildRequires: g++
BuildRequires: glib2-devel
BuildRequires: gsettings-desktop-schemas-devel
Requires:      gsettings-desktop-schemas
Requires:      glib2

%description
gsettings-ubuntu-touch-schemas contains a collection of GSettings schemas for
settings shared by various components of an Ubuntu environment.

%prep
%setup -q -c

%build
NOCONFIGURE=1 \
./autogen.sh

%configure

%make_build

%install
%make_install
rm -fv %{buildroot}%{_libdir}/*.la

pushd %{buildroot}/usr
find . ! -type d -exec ls {} + > %{_builddir}/%{name}-%{version}/files.txt
popd

sed -i s/^\.\\/// ./files.txt
sed -i 'sn^n%{_usr}/n' ./files.txt

%files -f files.txt
%license COPYING
%{_sharedstatedir}/polkit-1/localauthority/10-vendor.d/50-com.ubuntu.AccountsService.pkla

%changelog
