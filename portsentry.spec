Summary:	Port scan detection and active defense
Summary(pl):	Program wykrywaj±cy skanowanie portów i umo¿liwiaj±cy obronê
Name:		portsentry
Version:	1.1
Release:	11
License:	distributable (see LICENSE)
Group:		Applications/Networking
Source0:	http://www.psionic.com/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	782839446b7eca554bb1880ef0882670
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-logging-pld.patch
Patch1:		%{name}-ignore.csh.patch
Patch2:		%{name}-libwrap.patch
Patch3:		%{name}-config.patch
URL:		http://www.psionic.com/products/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	fileutils
Requires:	awk
Requires:	iproute2
Requires:	rc-scripts
Requires:	textutils
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
%patch2 -p1
%patch3 -p1

%build
%{__make} linux \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

%{__make} install \
	INSTALLDIR=$RPM_BUILD_ROOT/etc

install ignore.csh $RPM_BUILD_ROOT%{_sbindir}/portsentry-ignore
install portsentry $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portsentry
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/portsentry

touch $RPM_BUILD_ROOT%{_sysconfdir}/{portsentry.blocked.{audp,atcp,stcp,sudp,tcp,udp},portsentry.history}

# the portsentry binary
rm -f $RPM_BUILD_ROOT/etc/portsentry/portsentry

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/portsentry-ignore
/sbin/chkconfig --add portsentry
%service portsentry restart "portsentry daemon"

%preun
if [ "$1" = "0" ]; then
	%service portsentry stop
	/sbin/chkconfig --del portsentry
fi

%files
%defattr(644,root,root,755)
%doc README* CHANGES CREDITS LICENSE
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/portsentry.conf
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/portsentry.ignore
%attr(640,root,root) %ghost %{_sysconfdir}/portsentry.history
%attr(640,root,root) %ghost %{_sysconfdir}/portsentry.blocked*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_sbindir}/*
