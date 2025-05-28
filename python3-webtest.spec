#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	webtest
Summary:	Helper to test WSGI applications
Summary(pl.UTF-8):	Moduł pomocniczy do testowania aplikacji WSGI
Name:		python3-%{module}
Version:	3.0.4
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/webtest/
Source0:	https://files.pythonhosted.org/packages/source/W/WebTest/webtest-%{version}.tar.gz
# Source0-md5:	4481094708b9158cf124636172f8b24c
Patch0:		%{name}-deps.patch
URL:		http://webtest.pythonpaste.org/
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PasteDeploy
BuildRequires:	python3-WSGIProxy2
BuildRequires:	python3-WebOb >= 1.2
BuildRequires:	python3-bs4
BuildRequires:	python3-dtopt
BuildRequires:	python3-nose >= 1.3.1
BuildRequires:	python3-pyquery
BuildRequires:	python3-six
BuildRequires:	python3-waitress >= 0.8.5
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-docutils
BuildRequires:	python3-pylons-sphinx-themes >= 1.0.8
BuildRequires:	sphinx-pdg-3 >= 1.8.1
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebTest wraps any WSGI application and makes it easy to send test
requests to that application, without starting up an HTTP server.

This provides convenient full-stack testing of applications written
with any WSGI-compatible framework.

%description -l pl.UTF-8
WebTest obudowuje dowolną aplikację WSGI i ułatwia wysyłanie do niej
testowych żądań bez uruchamiania serwera HTTP.

Daje to wygodne, oparte o pełny stos testowanie aplikacji napisanych
przy użyciu dowolnego szkieletu zgodnego z WSGI.

%package apidocs
Summary:	API documentation for Python WebTest module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona WebTest
Group:		Documentation

%description apidocs
API documentation for Python WebTest module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona WebTest.

%prep
%setup -q -n webtest-%{version}
#%%patch -P 0 -p1

# Remove bundled egg info
%{__rm} -r *.egg-info

%build
%py3_build %{?with_tests:test}

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst license.rst
%{py3_sitescriptdir}/webtest
%{py3_sitescriptdir}/WebTest-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
