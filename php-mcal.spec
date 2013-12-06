%define realname MCAL
%define modname mcal
%define soname %{modname}.so
%define inifile 62_%{modname}.ini

Summary:	The %{realname} module for PHP
Name:		php-%{modname}
Epoch:		1
Version:	0.6
Release:	47
Group:		Development/PHP
License:	PHP License
Url:		http://www.php.net
Source0:	mcal-%{version}.tar.bz2
Patch0:		mcal-0.6-deprecation_fix.diff
Patch1:		mcal-0.6-php54x.diff
BuildRequires:	mcal-devel
BuildRequires:  php-devel >= 3:5.2.0

%description
This is a dynamic shared object (DSO) that adds MCAL support to PHP.

MCAL stands for Modular Calendar Access Library.
 
Libmcal is a C library for accessing calendars. It's written to be very
modular, with pluggable drivers. MCAL is the calendar equivalent of the IMAP
module for mailboxes.
 
With mcal support, a calendar stream can be opened much like the mailbox stream
with the IMAP support. Calendars can be local file stores, remote ICAP servers,
or other formats that are supported by the mcal library.
 
Calendar events can be pulled up, queried, and stored. There is also support
for calendar triggers (alarms) and recurring events.
 
With libmcal, central calendar servers can be accessed, removing the need for
any specific database or local file programming. 

%prep
%setup -qn mcal-%{version}
%patch0 -p0
%patch1 -p0

%build
%serverbuild

phpize
%configure2_5x \
	--with-libdir=%{_lib} \
	--with-%{modname}=%{_prefix}

%make
mv modules/*.so .

%install
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%files 
%doc README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

