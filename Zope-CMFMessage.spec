%define		zope_subname CMFMessage
Summary:	Product provides a 'Who Is Online'
Summary(pl):	Produkt umożliwiający sprawdzanie, kto jest zalogowany
Name:		Zope-%{zope_subname}
Version:	1.1
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/collective/%{zope_subname}-1_1.tgz
# Source0-md5:	fc38580a86005cf2781504ea9a400ec3
URL:		http://sourceforge.net/projects/collective/
Requires(post,postun):	/usr/sbin/installzopeproduct
BuildRequires:  python
%pyrequires_eq	python-modules
Requires:	Zope
Requires:	Zope-CMF
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Product provides a 'Who Is Online'.

%description -l pl
Produkt umożliwiający sprawdzanie, kto jest zalogowany.

%prep
%setup -q -c
find . -type f -name *.pyc | xargs rm -rf

%build
mkdir docs docs/CMFMessage docs/CMFUserTrackTool docs/UserTrack
mv -f CMFMessage/{AUTHORS,INSTALL,README} docs/CMFMessage
mv -f CMFUserTrackTool/{AUTHORS,readme.txt} docs/CMFUserTrackTool
mv -f UserTrack/{AUTHORS,readme.txt} docs/UserTrack
rm -rf {CMFUserTrackTool,UserTrack}/.cvsignore

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af * $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in CMFMessage CMFUserTrackTool UserTrack ; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
	for p in CMFMessage CMFUserTrackTool UserTrack ; do
		/usr/sbin/installzopeproduct -d $p
	done
fi
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}
