%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           jruby
Summary:        Pure-Java Implementation of the Ruby Programming Language
Version:        9.1.12.0
Release:        2%{dist}
Group:          Development/System
License:        Multiple
URL:            http://www.jruby.org
Source0:        %{name}-bin-%{version}.tar.gz
Source1:        jruby.profile

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

#Requires:      java-1.7.0-openjdk
Conflicts:      rubygem-jruby

%description
100% Pure-Java Implementation of the Ruby Programming Language

%prep
%setup -q

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/jruby
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

#remove windows support
find bin -type f -iname "*.bat" -delete
find bin -type f -iname "*.exe" -delete
find bin -type f -iname "*.dll" -delete

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/jruby
cp -a bin $RPM_BUILD_ROOT%{_datadir}/jruby/
cp -a lib $RPM_BUILD_ROOT%{_datadir}/jruby/

#only i386/x86_64 support
rm -rf $RPM_BUILD_ROOT%{_datadir}/jruby/lib/jni/*
rm -rf $RPM_BUILD_ROOT%{_datadir}/jruby/lib/ruby/stdlib/ffi/platform/*
mv lib/jni/i386-Linux   $RPM_BUILD_ROOT%{_datadir}/jruby/lib/jni/
mv lib/jni/x86_64-Linux $RPM_BUILD_ROOT%{_datadir}/jruby/lib/jni/
mv lib/ruby/stdlib/ffi/platform/i386-linux   $RPM_BUILD_ROOT%{_datadir}/jruby/lib/ruby/stdlib/ffi/platform/
mv lib/ruby/stdlib/ffi/platform/x86_64-linux $RPM_BUILD_ROOT%{_datadir}/jruby/lib/ruby/stdlib/ffi/platform/

%{__install} -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/jruby.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
source /etc/profile.d/jruby.sh || true

%files
%defattr(-,root,root,-)
%{_datadir}/jruby
%config(noreplace) %{_sysconfdir}/profile.d/jruby.sh
%license BSDL LICENSE.RUBY

%changelog
* Wed Aug 16 2017  Purple Grape <purplegrape4@gmail.com>
- jruby rpm init release 9.1.12.0
- only Linux i386/x86_64 support
