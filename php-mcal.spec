%define realname MCAL
%define modname mcal
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 62_%{modname}.ini

Summary:	The %{realname} module for PHP
Name:		php-%{modname}
Version:	0.6
Release:	%mkrel 16
Group:		Development/PHP
License:	PHP License
URL:		http://www.php.net
Source0:	mcal-%{version}.tar.bz2
BuildRequires:  php-devel >= 3:5.2.0
BuildRequires:	libmcal-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-root

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

%setup -q -n mcal-%{version}

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"

%if %mdkversion >= 200710
export CFLAGS="$CFLAGS -fstack-protector"
export CXXFLAGS="$CXXFLAGS -fstack-protector"
export FFLAGS="$FFLAGS -fstack-protector"
%endif

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
