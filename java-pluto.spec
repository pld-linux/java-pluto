#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	java_sun	# build using java-sun

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%include	/usr/lib/rpm/macros.java

%define		apiver	1.0
%define		srcname pluto
Summary:	Pluto portlet api
Name:		java-pluto
Version:	%{apiver}.1
Release:	4
License:	Apache v2.0
Group:		Libraries/Java
Source0:	%{srcname}-%{version}.tar.bz2
# Source0-md5:	d6355e173ebda88b4a2da4f7df688875
URL:		http://portals.apache.org/pluto/
BuildRequires:	ant
%{?with_java_sun:BuildRequires:	java-sun}
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Provides:	java(Portlet) = %{apiver}
Obsoletes:	java-portletapi10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Interfaces for pluto portlet implementation.

%package javadoc
Summary:	Online manual for portletapi
Summary(pl.UTF-8):	Dokumentacja online do portletapi
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for portletapi.

%description javadoc -l pl.UTF-8
Dokumentacja do portletapi.

%prep
%setup -q -n pluto-%{version}

%build

cd api
%ant \
    -Dbuild.sysclasspath=only \
    jar

%{?with_javadoc:%ant -Dnoget=1 javadoc}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

install api/target/portlet-api-%{apiver}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# P: java(portlet) = 1.0
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/portlet-api-%{apiver}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a api/dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
