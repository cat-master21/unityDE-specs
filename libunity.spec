Name:	 libunity
Summary: Library for integrating with Unity and Plasma
Version: 7.1.4
Release: 1

# most files LGPLv3, with a handful of GPLv3 (unity-sound-menu* sources in particular)
License: GPLv3
URL:	 https://launchpad.net/libunity
# same sources as shipped in ubuntu packages
Source0: https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/libunity/%{version}+19.04.20190319-0ubuntu1/libunity_%{version}+19.04.20190319.orig.tar.gz
Patch0:  https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/libunity/%{version}+19.04.20190319-0ubuntu1/libunity_%{version}+19.04.20190319-0ubuntu1.diff.gz

Patch0001:  https://launchpadlibrarian.net/443817430/0001-Fix-FTB-with-recent-vala-requiring-non-public-abstra.patch
# Patch for vala 0.53.2 portability
Patch2:  https://src.fedoraproject.org/rpms/libunity/raw/rawhide/f/libunity-7.1.4-vala-053.patch

BuildRequires: automake libtool gnome-common
BuildRequires: intltool
BuildRequires: pkgconfig(dee-1.0)
BuildRequires: pkgconfig(dbusmenu-glib-0.4)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: python3-devel python3
BuildRequires: vala
BuildRequires: make

%description
A library for instrumenting and integrating with all aspects of the Unity
shell devel version with headers. Thanks to https://src.fedoraproject.org/rpms/libunity for the original RPM spec.

%package devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package -n python3-libunity
Summary: Python3 bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3-gobject-base
%description -n python3-libunity
%{summary}.


%prep
%setup -q -c
%patch0 -p1
%patch1 -p1 -b .0001
%patch2 -p1 -b .vala_053


%build
NOCONFIGURE=1 \
./autogen.sh

PYTHON=%{__python3}
export PYTHON

%configure \
  --disable-schemas-compile \
  --disable-silent-rules \
  --disable-static

%make_build


%install
%make_install

## unpackaged files
# libtool, unused lib symlink
rm -fv \
  %{buildroot}%{_libdir}/lib*.la \
  %{buildroot}%{_libdir}/libunity/*.{la,so}

%py_byte_compile %{__python3} %{buildroot}%{python3_sitearch}/gi/overrides/

%ldconfig_post

%postun
%{?ldconfig}
%if 0%{?rhel} && 0%{?rhel} < 8
if [ $1 -eq 0 ]; then
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%endif

%files
%doc AUTHORS README
%license COPYING*
%{_bindir}/libunity-tool
%{_bindir}/unity-scope-loader
%{_libdir}/libunity.so.9*
%{_libdir}/libunity-extras.so.9*
%{_libdir}/girepository-1.0/Unity-7.0.typelib
%{_libdir}/girepository-1.0/UnityExtras-7.0.typelib
%dir %{_libdir}/libunity/
%{_libdir}/libunity/libunity-protocol-private.so.*
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.Lenses.gschema.xml
%{_datadir}/unity/
%{_datadir}/unity-scopes/

%files -n python3-libunity
%{python3_sitearch}/gi/overrides/Unity.py*
%{python3_sitearch}/gi/overrides/__pycache__/*

%files devel
%{_includedir}/unity/
%{_libdir}/libunity.so
%{_libdir}/libunity-extras.so
%{_libdir}/pkgconfig/unity.pc
%{_libdir}/pkgconfig/unity-extras.pc
%{_libdir}/pkgconfig/unity-protocol-private.pc
%{_datadir}/gir-1.0/Unity-7.0.gir
%{_datadir}/gir-1.0/UnityExtras-7.0.gir
%{_datadir}/vala/vapi/unity.*
%{_datadir}/vala/vapi/unity-extras.*
%{_datadir}/vala/vapi/unity-protocol.*
%{_datadir}/vala/vapi/unity-trace.*


%changelog
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-30.20190319
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 7.1.4-29.20190319
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-28.20190319
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 13 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 7.1.4-27.20190319
- Patch for vala 0.53.2 portability

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-26.20190319
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 7.1.4-25.20190319
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-24.20190319
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 07 2020 Than Ngo <than@redhat.com> - 7.1.4-23.20190319
- Fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-22.20190319
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-21.20190319
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 7.1.4-20.20190319
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-19.20190319
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Rex Dieter <rdieter@fedoraproject.org> - 7.1.4-18.20190319
- pull in upstream FTBFS fix

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 7.1.4-17.20190319
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-16.20190319
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Rex Dieter <rdieter@fedoraproject.org> - 7.1.4-15.20190319
- rebuild

* Sun Apr 28 2019 Rex Dieter <rdieter@fedoraproject.org> - 7.1.4-14.20190319
- 20190319 snapshot used by ubuntu

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-13.20180209
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 15 2018 Rex Dieter <rdieter@fedoraproject.org> - 7.1.4-12.20180209
- 20180209 snapshot used by ubuntu
- use %%make_build %%make_install %%ldconfig

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-11.20151002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 7.1.4-10.20151002
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-9.20151002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-8.20151002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-7.20151002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-6.20151002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 7.1.4-5.20151002
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.4-4.20151002
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 7.1.4-3.20151002
- rebuild

* Thu Feb 11 2016 Rex Dieter <rdieter@fedoraproject.org> 7.1.4-2.20151002
- update summary/description
- support python3
- make glib-compile-schemas scriptlet conditional (< f24 only)
- include snapshot date in Release:

* Wed Feb 10 2016 Rex Dieter <rdieter@fedoraproject.org> 7.1.4-1
- first try

