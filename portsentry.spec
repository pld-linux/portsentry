Summary:	Port scan detection and active defense
Summary(pl):	Program wykrywaj�cy skanowanie port�w i umo�liwiaj�cy obron�
Name:		portsentry
Version:	1.0
Release:	3
License:	distributable (see LICENSE)
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Source0:	http://www.psionic.com/tools/%{name}-%{version}.tar.gz
Source1:	portsentry.init
Source2:	portsentry.sysconfig
Patch0:		%{name}-pld.patch
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
%patch0 -p1 

%build
make linux CFLAGS="$RPM_OPT_FLAGS -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

make install INSTALLDIR=$RPM_BUILD_ROOT
install ignore.sh $RPM_BUILD_ROOT%{_bindir}
strip $RPM_BUILD_ROOT%{_bindir}/portsentry

gzip -9nf README* CHANGES CREDITS LICENSE

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portsentry
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/portsentry

%clean
rm -rf $RPM_BUILD_ROOT

%post -n portsentry
%{_bindir}/ignore.sh
/sbin/chkconfig --add portsentry
ls --color=none /var/lock/subsys/portsentry* >/dev/null 2>&1
if [ $? -eq "0" ]; then
	/etc/rc.d/init.d/portsentry restart >&2
else
	echo "Run \"/etc/rc.d/init.d/portsentry start\" to start portsentry daemon."
fi

%preun -n portsentry
if [ "$1" = "0" ]; then
	ls --color=none /var/lock/subsys/portsentry* >/dev/null 2>&1
	if [ $? -eq "0" ]; then
		/etc/rc.d/init.d/portsentry stop >&2
	fi
	/sbin/chkconfig --del portsentry
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/portsentry.conf
%attr(640,root,root) %config(noreplace missingok) %{_sysconfdir}/portsentry.ignore
%attr(755,root,root) %{_bindir}/*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*
%attr(754,root,root) /etc/rc.d/init.d/*
