Summary:	Port scan detection and active defense.
Summary(pl):	Program wykrywaj±cy skanowanie portów i umo¿liwiaj±cy obronê
Name:		portsentry
Version:	1.0
Release:	1
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Copyright:	GPL
Source0:	portsentry-1.0.tar.gz
URL:		www.psionic.com/tools/portsentry/
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
PortSentry is part of the Abacus Project suite of tools. The Abacus
Project is an initiative to release low-maintenance, generic, and reliable
host based intrusion detection software to the Internet community. More
information can be obtained from http://www.psionic.com.

%description -l pl
PortSentry jest czê¶ci± zestawu narzêdzi Projektu Abacus. Projekt
Abacus ma na celu stworzenie ogólnego, pewnego i wymagaj±cego
niewielkiej obs³ugi oprogramowania do wykrywania prób skanowania
portów dla internetowej spo³eczno¶ci. Wiêcej informacji mo¿na znale¼æ
pod adresem http://www.psionic.com.

%prep
%setup  -q

%build

LDFLAGS="-s" ; export LDFLAGS

make linux

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
install {README*,CHANGES,CREDITS,LICENSE} $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
make install INSTALLDIR=$RPM_BUILD_ROOT
install ignore.sh $RPM_BUILD_ROOT%{_bindir}

%post

%{_bindir}/ignore.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) /etc/portsentry/portsentry.conf
%config(noreplace missingok) /etc/portsentry/portsentry.ignore
%attr(755,root,root) /usr/bin/portsentry
%doc %{_defaultdocdir}/%{name}-%{version}/*
%attr(755,root,root) %{_bindir}/ignore.sh
