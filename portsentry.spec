Summary:	Port scan detection and active defense
Summary(pl):	Program wykrywaj±cy skanowanie portów i umo¿liwiaj±cy obronê
Name:		portsentry
Version:	1.1
Release:	10
License:	distributable (see LICENSE)
Group:		Applications/Networking
Source0:	http://www.psionic.com/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	782839446b7eca554bb1880ef0882670
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-logging-pld.patch
Patch1:		%{name}-ignore.csh.patch
URL:		http://www.psionic.com/products/
PreReq:		rc-scripts
PreReq:		/bin/awk
PreReq:		/bin/csh
PreReq:		iproute2
PreReq:		textutils
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/portsentry

%description
PortSentry is part of the Abacus Project suite of tools. The Abacus
Project is an initiative to release low-maintenance, generic, and
reliable host based intrusion detection software to the Internet
community.

%description -l pl
PortSentry jest czê¶ci± zestawu narzêdzi Projektu Abacus. Projekt
Abacus ma na celu stworzenie ogólnego, pewnego i wymagaj±cego
niewielkiej obs³ugi oprogramowania do wykrywania prób skanowania
portów dla internetowej spo³eczno¶ci.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
%{__sed} -i -e 's@\/etc\/hosts.deny@\/etc\/tcpd\/hosts.deny@' portsentry_config.h
%{__make} linux \
	CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/{rc.d/init.d,sysconfig}}

%{__make} install \
	INSTALLDIR=$RPM_BUILD_ROOT/etc

install ignore.csh $RPM_BUILD_ROOT%{_bindir}
install portsentry $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portsentry
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/portsentry


%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/ignore.csh
/sbin/chkconfig --add portsentry
ls --color=none /var/lock/subsys/portsentry* >/dev/null 2>&1
if [ $? -eq "0" ]; then
	/etc/rc.d/init.d/portsentry restart >&2
else
	echo "Run \"/etc/rc.d/init.d/portsentry start\" to start portsentry daemon."
fi

%preun
if [ "$1" = "0" ]; then
	ls --color=none /var/lock/subsys/portsentry* >/dev/null 2>&1
	if [ $? -eq "0" ]; then
		/etc/rc.d/init.d/portsentry stop >&2
	fi
	/sbin/chkconfig --del portsentry
fi

%files
%defattr(644,root,root,755)
%doc README* CHANGES CREDITS LICENSE
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/portsentry.conf
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 size mtime) %{_sysconfdir}/portsentry.ignore
%attr(640,root,root) %config %verify(not md5 size mtime) /etc/sysconfig/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_bindir}/*
