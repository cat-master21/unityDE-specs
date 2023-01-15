%global forgeurl https://gitlab.com/vala-panel-project/vala-panel-appmenu
%global commit 99cd56c1644fe4193854902c450e67f9a6685112

%forgemeta

Name:    vala-panel-appmenu
Version: 0.7.6
Release: 1%{?dist}
License: LGPL-3.0+
Summary: This package provides Application Menu plugin for vala-panel
URL:     %{forgeurl}

Source: %{forgesource}

BuildRequires: bamf-daemon
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: gettext
BuildRequires: vala >= 0.32.0
BuildRequires: pkgconfig(gtk+-2.0) >= 2.24.0
BuildRequires: pkgconfig(gtk+-3.0) >= 3.20.0
BuildRequires: pkgconfig(libpeas-1.0) >= 1.2.0
BuildRequires: pkgconfig(libbamf3)
BuildRequires: pkgconfig(libxfce4panel-2.0)
BuildRequires: pkgconfig(libxfconf-0)
BuildRequires: pkgconfig(libwnck-3.0) >= 3.4.0
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(dbusmenu-glib-0.4)

Provides: vala-panel-appmenu-plugin

Requires: bamf-daemon
Requires: libdbusmenu
Requires: libdbusmenu-gtk2
Requires: libdbusmenu-gtk3
Requires: libappmenu-gtk2-parser
Requires: libappmenu-gtk3-parser
Requires: appmenu-gtk-module-common
Requires: appmenu-gtk2-module
Requires: appmenu-gtk3-module
Requires: appmenu-qt5

%description
This is Application Menu (Global Menu) plugin.
It built using Unity protocol and libraries,
and share all Unity limitations and advancements.


%package -n xfce4-vala-panel-appmenu-plugin
Summary:    This package provides Application Menu plugin for xfce4-panel
Requires:   bamf-daemon
Requires:   libdbusmenu
Requires:   libdbusmenu-gtk2
Requires:   libdbusmenu-gtk3
Requires:   appmenu-gtk-module-common
Requires:   appmenu-gtk2-module
Requires:   appmenu-gtk3-module
Requires:   appmenu-qt5

%description -n xfce4-vala-panel-appmenu-plugin
This is Application Menu (Global Menu) plugin.
It built using Unity protocol and libraries,
and share all Unity limitations and advancements.

%package -n    libappmenu-gtk-parser-devel
Summary:       Common development-files for libappmenu-gtk{2,3}-parser
BuildArch:     noarch
BuildRequires: gtk-doc
Requires:      gtk-doc

%description -n libappmenu-gtk-parser-devel
This package contains common headers and documentation for
libappmenu-gtk{2,3}-parser.


%package -n    libappmenu-gtk2-parser
Summary:       Gtk2MenuShell to GMenuModel parser
BuildRequires: pkgconfig(gtk+-2.0)

%description -n libappmenu-gtk2-parser
This library converts Gtk2MenuShells into GMenuModels.


%package -n libappmenu-gtk2-parser-devel
Summary:    Development-files for libappmenu-gtk2-parser
Requires:   pkgconfig(gtk+-2.0)%{?_isa}
Requires:   libappmenu-gtk-parser-devel == %{version}-%{release}
Requires:   libappmenu-gtk2-parser%{?_isa} == %{version}-%{release}

%description -n libappmenu-gtk2-parser-devel
This package contains development-files for libappmenu-gtk2-parser.


%package -n    libappmenu-gtk3-parser
Summary:       Gtk3MenuShell to GMenuModel parser
BuildRequires: pkgconfig(gtk+-3.0)

%description -n libappmenu-gtk3-parser
This library converts Gtk3MenuShells into GMenuModels.


%package -n libappmenu-gtk3-parser-devel
Summary:    Development-files for libappmenu-gtk3-parser
Requires:   pkgconfig(gtk+-3.0)%{?_isa}
Requires:   libappmenu-gtk-parser-devel == %{version}-%{release}
Requires:   libappmenu-gtk3-parser%{?_isa} == %{version}-%{release}

%description -n libappmenu-gtk3-parser-devel
This package contains development-files for libappmenu-gtk3-parser.


%package -n    appmenu-gtk-module-common
Summary:       Common files for appmenu-gtk{2,3}-module
BuildRequires: systemd

%description -n appmenu-gtk-module-common
This package contains common data-files for appmenu-gtk{2,3}-module.


%package -n appmenu-gtk2-module
Summary:    Gtk2MenuShell D-Bus exporter
Requires:   libappmenu-gtk2-parser%{?_isa} == %{version}-%{release}
Requires:   appmenu-gtk-module-common == %{version}-%{release}
Provides:   appmenu-gtk == %{version}-%{release}
Provides:   appmenu-gtk%{?_isa} == %{version}-%{release}

%description -n appmenu-gtk2-module
This GTK 2 module exports Gtk2MenuShells over D-Bus.


%package -n appmenu-gtk3-module
Summary:    Gtk3MenuShell D-Bus exporter
Requires:   libappmenu-gtk3-parser%{?_isa} == %{version}-%{release}
Requires:   appmenu-gtk-module-common == %{version}-%{release}
Provides:   appmenu-gtk3 == %{version}-%{release}
Provides:   appmenu-gtk3%{?_isa} == %{version}-%{release}


%description -n appmenu-gtk3-module
This GTK 3 module exports Gtk3MenuShells over D-Bus.


%prep
%forgeautosetup -p1

%build
%meson -Dxfce=enabled -Dvalapanel=enabled -Djayatana=enabled \
       -Dbudgie=enabled -Dmate=enabled -Dappmenu-gtk-module=enabled \
%meson_build

%install
%meson_install
%find_lang %{name}

%{__mkdir} -p %{buildroot}%{_userunitdir}/default.target.wants
%{_bindir}/ln -s %{_userunitdir}/%{name}.service \
                %{buildroot}%{_userunitdir}/default.target.wants/%{name}.service

%post -n   libappmenu-gtk2-parser -p /sbin/ldconfig
%postun -n libappmenu-gtk2-parser -p /sbin/ldconfig

%post -n   libappmenu-gtk3-parser -p /sbin/ldconfig
%postun -n libappmenu-gtk3-parser -p /sbin/ldconfig

%postun -n appmenu-gtk-module-common
if [ $1 -eq 0 ] ; then
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n appmenu-gtk-module-common
%{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun -n appmenu-gtk2-module
%{_bindir}/gtk-query-immodules-2.0-%{__isa_bits} --update-cache &> /dev/null || :

%post -n appmenu-gtk2-module
if [ $1 -eq 1 ] ; then
    %{_bindir}/gtk-query-immodules-2.0-%{__isa_bits} --update-cache &> /dev/null || :
fi

%postun -n appmenu-gtk3-module
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache &> /dev/null || :

%post -n appmenu-gtk3-module
if [ $1 -eq 1 ] ; then
    %{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache &> /dev/null || :
fi

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_userunitdir}/default.target.wants/%{name}.service

%files -n xfce4-vala-panel-appmenu-plugin
%{_libdir}/xfce4/panel/plugins/libappmenu-xfce.so
%{_datadir}/xfce4/panel/plugins/appmenu.desktop

%files -n libappmenu-gtk-parser-devel
%{_includedir}/appmenu-gtk-parser

%files -n libappmenu-gtk2-parser
%license LICENSE*
%{_libdir}/libappmenu-gtk2-parser.so.*

%files -n libappmenu-gtk2-parser-devel
%{_libdir}/libappmenu-gtk2-parser.so
%{_libdir}/pkgconfig/appmenu-gtk2-parser.pc

%files -n libappmenu-gtk3-parser
%license LICENSE
%{_libdir}/libappmenu-gtk3-parser.so.*

%files -n libappmenu-gtk3-parser-devel
%{_libdir}/libappmenu-gtk3-parser.so
%{_libdir}/pkgconfig/appmenu-gtk3-parser.pc

%files -n appmenu-gtk-module-common
%license LICENSE
%{_libexecdir}/vala-panel/appmenu-registrar
%{_datadir}/dbus-1/services/com.canonical.AppMenu.Registrar.service
%{_datadir}/glib-2.0/schemas/*
%{_userunitdir}/appmenu-gtk-module.service
%{_docdir}/appmenu-gtk-module/*
%{_datadir}/licenses/appmenu-gtk-module/*

%files -n appmenu-gtk2-module
%{_libdir}/gtk-2.0/modules/libappmenu-gtk-module.so

%files -n appmenu-gtk3-module
%{_libdir}/gtk-3.0/modules/libappmenu-gtk-module.so

%changelog
%autochangelog
