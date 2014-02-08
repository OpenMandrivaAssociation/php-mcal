%define realname MCAL
%define modname mcal
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 62_%{modname}.ini

Summary:	The %{realname} module for PHP
Name:		php-%{modname}
Version:	0.6
Release:	47
Group:		Development/PHP
License:	PHP License
URL:		http://www.php.net
Source0:	mcal-%{version}.tar.bz2
Patch0:		mcal-0.6-deprecation_fix.diff
Patch1:		mcal-0.6-php54x.diff
BuildRequires:  php-devel >= 3:5.2.0
BuildRequires:	mcal-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch0 -p0
%patch1 -p0

%build
%serverbuild

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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Wed May 02 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-45mdv2012.0
+ Revision: 795033
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-44
+ Revision: 761119
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-43
+ Revision: 696370
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-42
+ Revision: 695314
- rebuilt for php-5.3.7

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-41
+ Revision: 667481
- mass rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-40
+ Revision: 646554
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-39mdv2011.0
+ Revision: 629740
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-38mdv2011.0
+ Revision: 628046
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-37mdv2011.0
+ Revision: 600178
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-36mdv2011.0
+ Revision: 588715
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-35mdv2010.1
+ Revision: 514570
- rebuilt for php-5.3.2

* Mon Feb 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-34mdv2010.1
+ Revision: 509468
- rebuild
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-32mdv2010.1
+ Revision: 485261
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-31mdv2010.1
+ Revision: 468088
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-30mdv2010.0
+ Revision: 451218
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:0.6-29mdv2010.0
+ Revision: 397552
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-28mdv2010.0
+ Revision: 375360
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-27mdv2009.1
+ Revision: 346515
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-26mdv2009.1
+ Revision: 341511
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-25mdv2009.1
+ Revision: 321791
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-24mdv2009.1
+ Revision: 310220
- rebuilt against php-5.2.7

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-23mdv2009.0
+ Revision: 235879
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-22mdv2009.0
+ Revision: 200115
- rebuilt against php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-21mdv2008.1
+ Revision: 161988
- rebuild
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-19mdv2008.1
+ Revision: 107572
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-18mdv2008.0
+ Revision: 77459
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-17mdv2008.0
+ Revision: 64303
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-16mdv2008.0
+ Revision: 39386
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-15mdv2008.0
+ Revision: 33781
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-14mdv2008.0
+ Revision: 21030
- rebuilt against new upstream version (5.2.2)


* Sun Mar 18 2007 Pascal Terjan <pterjan@mandriva.org> 0.6-13mdv2007.1
+ Revision: 145672
- Rebuild for new mcal

* Fri Feb 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-12mdv2007.1
+ Revision: 118556
- rebuilt against new upstream php version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-11mdv2007.0
+ Revision: 78210
- fix deps

* Tue Nov 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-10mdv2007.1
+ Revision: 77369
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-9mdv2007.1
+ Revision: 75270
- Import php-mcal

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-9
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-8mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-7mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-6mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-5mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-4mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-3mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-2mdk
- rebuilt against php-5.1.0

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.6-1mdk
- rebuilt against php-5.1.0RC4
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.6-0.RC1.2mdk
- rebuilt to provide a -debug package too

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.6-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5_0.6-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.6-2mdk
- make a tar ball from the php4 source, this prevents php4-devel to
  end up in main (pterjan)

* Tue Aug 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.6-1mdk
- fix version

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-1mdk
- build for php-5.0.4 using the source from php-4.4.0, the 
  changelog for php5 says it is moved to pecl now, but i could 
  not find it...

* Tue Jul 12 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-1mdk
- rebuilt for php-4.4.0 final

* Wed Jul 06 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-0.RC2.1mdk
- rebuilt for php-4.4.0RC2

* Wed Jun 15 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-0.RC1.1mdk
- rebuilt for php-4.4.0RC1

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11-1mdk
- renamed to php4-*

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11-1mdk
- 4.3.11

* Mon Mar 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10-4mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10-3mdk
- rebuilt against a non hardened-php aware php lib

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10-1mdk
- rebuild for php 4.3.10

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9-1mdk
- rebuild for php 4.3.9

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6-1mdk
- move scandir to /etc/php4.d

