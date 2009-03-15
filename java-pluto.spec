#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	java_sun	# build using java-sun

%include	/usr/lib/rpm/macros.java

%define		apiver	1.0
%define		srcname portletapi10
Summary:	portlet api
Name:		java-portletapi10
Version:	%{apiver}.1
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	pluto-%{version}.tar.bz2
# Source0-md5:	d6355e173ebda88b4a2da4f7df688875
URL:		http://portals.apache.org/pluto/
BuildRequires:	ant
%{?with_java_sun:BuildRequires:	java-sun}
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pluto libraries

%description -l pl.UTF-8
Pluto libraries

%package portletapi
Summary:	Portlet api
Group:		Libraries/Java
Requires:	jpackage-utils

%description portletapi
Portlet api

%package javadoc
Summary:	Online manual for pluto libraries
Summary(pl.UTF-8):	Dokumentacja online do bibliotek pluto
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for pluto libraries.

%description javadoc -l pl.UTF-8
Dokumentacja do bibliotek pluto.

%prep
%setup -q -n pluto-%{version}

%build

cd api
%ant \
    -Dbuild.sysclasspath=only \
    %{!?with_java_sun:-Dbuild.compiler=extJavac} \
    jar

%{?with_javadoc:%ant -Dnoget=1 javadoc}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

install api/target/portlet-api-%{apiver}.jar $RPM_BUILD_ROOT%{_javadir}/portletapi10-%{apiver}.jar
ln -s portletapi10-%{apiver}.jar $RPM_BUILD_ROOT%{_javadir}/portletapi10.jar

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
