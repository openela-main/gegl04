%global apiver 0.4

Name:                 gegl04
Version:              0.4.4
Release:              7%{?dist}
Summary:              Graph based image processing framework

# The binary is under the GPL, while the libs are under LGPL.
# The main package only installs the libs, which makes the license:
License:              LGPLv3+
URL:                  http://www.gegl.org/
Source0:              http://download.gimp.org/pub/gegl/%{apiver}/gegl-%{version}.tar.bz2

Patch1:               gegl-CVE-2021-45463.patch

BuildRequires:        chrpath
BuildRequires:        enscript
BuildRequires:        gcc-c++
BuildRequires:        gettext-devel >= 0.19.8
BuildRequires:        gobject-introspection-devel >= 1.32.0
BuildRequires:        libspiro-devel
BuildRequires:        perl-interpreter
BuildRequires:        ruby
BuildRequires:        SDL-devel >= 1.2.0
BuildRequires:        suitesparse-devel
BuildRequires:        vala-tools

BuildRequires:        pkgconfig(babl) >= 0.1.52
BuildRequires:        pkgconfig(cairo) >= 1.12.2
BuildRequires:        compat-exiv2-026
BuildRequires:        pkgconfig(gdk-pixbuf-2.0) >= 2.32.0
BuildRequires:        pkgconfig(glib-2.0) >= 2.44.0
BuildRequires:        pkgconfig(jasper) >= 1.900.1
BuildRequires:        pkgconfig(json-glib-1.0)
BuildRequires:        pkgconfig(lcms2) >= 2.8
BuildRequires:        pkgconfig(lensfun) >= 0.2.5
BuildRequires:        pkgconfig(libraw) >= 0.19.0
BuildRequires:        pkgconfig(libpng) >= 1.6.0
BuildRequires:        pkgconfig(librsvg-2.0) >= 2.40.6
BuildRequires:        pkgconfig(libv4l2) >= 1.0.1
BuildRequires:        pkgconfig(libwebp) >= 0.5.0
BuildRequires:        pkgconfig(lua) >= 5.1.0
BuildRequires:        pkgconfig(OpenEXR) >= 1.6.1
BuildRequires:        pkgconfig(pango) >= 1.38.0
BuildRequires:        pkgconfig(pangocairo) >= 1.38.0
BuildRequires:        pkgconfig(pygobject-3.0) >= 3.2
BuildRequires:        pkgconfig(vapigen) >= 0.20.0
BuildRequires:        pkgconfig(libtiff-4) >= 4.0.0

# gegl contains a stripped down version of poly2tri-c, a C+glib port of
# poly2tri, a 2D constrained Delaunay triangulation library.
# Version information:
#     CURRENT REVISION: b27c5b79df2ffa4e2cb37f9e5536831f16afb11b
#     CACHED ON: August 11th, 2012
Provides:             bundled(poly2tri-c)


%description
GEGL (Generic Graphics Library) is a graph based image processing framework.
GEGLs original design was made to scratch GIMP's itches for a new
compositing and processing core. This core is being designed to have
minimal dependencies and a simple well defined API.


%package        devel
Summary:              Development files for %{name}
Requires:             %{name}%{?_isa} = %{version}-%{release}
Obsoletes:            %{name}-devel < 0.4.2
Conflicts:            %{name}-devel < 0.4.2

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use GEGL API version %{apiver}.


%package        devel-docs
Summary:              Documentation files for developing with %{name}
Requires:             %{name}%{?_isa} = %{version}-%{release}
Obsoletes:            %{name}-devel < 0.4.2
Conflicts:            %{name}-devel < 0.4.2
Conflicts:            gegl-devel < 0.4

%description    devel-docs
The %{name}-devel-docs package contains documentation files for developing
applications that use GEGL API version %{apiver}.


%package        tools
Summary:              Command line tools for %{name}
Requires:             %{name}%{?_isa} = %{version}-%{release}
License:              GPLv3+
Conflicts:            gegl < 0.4

%description    tools
The %{name}-tools package contains tools for the command line that use the
GEGL library.


%prep
%setup -q -n gegl-%{version}
%patch1 -p1 -b .CVE-2021-45463

%build
%configure --disable-static
make %{?_smp_mflags}


%install
%make_install

# Remove rpaths
chrpath --delete %{buildroot}%{_bindir}/*
chrpath --delete %{buildroot}%{_libdir}/*.so*
chrpath --delete %{buildroot}%{_libdir}/gegl-%{apiver}/*.so

# Remove .la files
find %{buildroot} -name '*.la' -delete

%find_lang gegl-%{apiver}


%ldconfig_scriptlets


%files -f gegl-%{apiver}.lang
%license COPYING.LESSER
%{_libdir}/gegl-%{apiver}/
%{_libdir}/libgegl-%{apiver}.so.*
%{_libdir}/libgegl-npd-%{apiver}.so
%{_libdir}/libgegl-sc-%{apiver}.so
%{_libdir}/girepository-1.0/Gegl-%{apiver}.typelib

%files devel
%{_includedir}/gegl-%{apiver}/
%{_libdir}/libgegl-%{apiver}.so
%{_libdir}/pkgconfig/gegl-%{apiver}.pc
%{_libdir}/pkgconfig/gegl-sc-%{apiver}.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Gegl-%{apiver}.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gegl-%{apiver}.deps
%{_datadir}/vala/vapi/gegl-%{apiver}.vapi

%files devel-docs
%doc %{_datadir}/gtk-doc/

%files tools
%license COPYING
%{_bindir}/*


%changelog
* Tue Jan 11 2022 Josef Ridky <jridky@redhat.com> - 0.4.4-7
- Fix CVE-2021-45463 (#2035424)

* Wed Oct 03 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.4.4-6
- Rebuild against new LibRaw soname
Resolves:             #1633708

* Thu Aug 23 2018 Josef Ridky <jridky@redhat.com> - 0.4.4-5
- Remove ImageMagick requirement
Resolves:             #1620209

* Mon Aug 06 2018 Josef Ridky <jridky@redhat.com> - 0.4.4-4
- Remove luajit requirement, because it is not available on RHEL-8
Resolves:             #1609985

* Thu Jul 19 2018 Christian Dersch <lupinix@fedoraproject.org> - 0.4.4-3
- Rebuilt for LibRaw soname bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.4-1
- version 0.4.4

* Mon May 21 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.2-2
- split off devel docs
- let gegl04-devel-docs explicitly conflict with old gegl-devel (#1577595)

* Mon May 21 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.2-1
- version 0.4.2

* Wed May 02 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.0-2
- don't require asciidoc for building
- always install unversioned executables

* Sat Apr 28 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.0-1
- import into Fedora dist-git

* Fri Apr 27 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.0-0.4
- own all created directories
- remove rpaths

* Fri Apr 27 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.0-0.3
- use %%ldconfig_scriptlets macro

* Fri Apr 27 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.0-0.2
- add tools subpackage
- tidy up remains of 0.3
- add back gtk-doc documentation

* Fri Apr 27 2018 Nils Philippsen <nils@tiptoe.de> - 0.4.0-0.1
- initial import
