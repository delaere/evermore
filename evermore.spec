%define name evermore
%define version 1.0.0
%define unmangled_version 1.0.0
%define unmangled_version 1.0.0
%define release 1

Summary: A tool to export data from Evernote to a semantic filesystem
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv3
Group: Applications/Productivity
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Christophe Delaere <christophe.delaere@gmail.com>
Provides: evermore = 1.0.0
Requires: TMSU python2-lxml python-html2text
Url: https://github.com/delaere/evermore

%description

A tool to export data from Evernote (more precisely NixNote) 
to a directory structure indexed with TMSU.

Notes are converted to markdown and attachments are saved. 
Every file is indexed with the tags from the related note.

~~~~
Usage: evermore.py [options] source.nnex destdir

Options:
  -h, --help     show this help message and exit
  -d, --dry      dry run (do not create files nor touch the database)
  -v, --verbose  verbose mode
~~~~
    

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES

%defattr(-,root,root)

%changelog
* Sat Dec 24 2016 Christophe Delaere <christophe.delaere@gmail.com> - 1.0.0-1
- Initial packaging.
