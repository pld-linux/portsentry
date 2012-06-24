Summary:	Port scan detection and active defense.
Summary(pl):	Program wykrywaj�cy skanowanie port�w i umo�liwiaj�cy obron�
Name:		portsentry
Version:	1.0
Release:	1
License:	distributable (see LICENSE)
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Source0:	http://www.psionic.com/tools/%{name}-%{version}.tar.gz
URL:		http://www.psionic.com/tools/portsentry/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/portsentry
%description
PortSentry is part of the Abacus Project suite of tools. The Abacus Project
is an initiative to release low-maintenance, generic, and reliable host
based intrusion detection software to the Internet community.

%description -l pl
PortSentry jest cz�ci� zestawu narz�dzi Projektu Abacus. Projekt Abacus ma
na celu stworzenie og�lnego, pewnego i wymagaj�cego niewielkiej obs�ugi
oprogramowania do wykrywania pr�b skanowania port�w dla internetowej
spo�eczno�ci.

%prep
%setup  -q

%build
make linux CFLAGS="$RPM_OPT_FLAGS -Wall"

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALLDIR=$RPM_BUILD_ROOT
install ignore.sh $RPM_BUILD_ROOT%{_bindir}

strip $RPM_BUILD_ROOT%{_bindir}/portsentry

gzip -9nf README* CHANGES CREDITS LICENSE

%post
%{_bindir}/ignore.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/portsentry.conf
%attr(640,root,root) %config(noreplace missingok) %{_sysconfdir}/portsentry.ignore
%attr(755,root,root) %{_bindir}/*
