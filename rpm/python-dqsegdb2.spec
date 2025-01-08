%define srcname dqsegdb2
%global distname %{lua:name = string.gsub(rpm.expand("%{srcname}"), "[.-]", "_"); print(name)}
%define version 1.3.0
%define release 1

Name:     python-%{srcname}
Version:  %{version}
Release:  %{release}%{?dist}
Summary:  Simplified python interface to DQSEGDB

License:  GPLv3
Url:      https://pypi.org/project/%{srcname}/
Source0:  %pypi_source %distname

Packager: Duncan Macleod <duncan.macleod@ligo.org>
Vendor:   Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch
Prefix:    %{_prefix}

# -- build requirements -----

# static build requirements
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
BuildRequires: pyproject-rpm-macros
%endif
BuildRequires: python%{python3_pkgversion}-devel >= 3.6
BuildRequires: python%{python3_pkgversion}-pip
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-setuptools_scm
BuildRequires: python%{python3_pkgversion}-wheel
# for man pages:
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
BuildRequires: python%{python3_pkgversion}-click
BuildRequires: python%{python3_pkgversion}-click-man
BuildRequires: python%{python3_pkgversion}-igwn-auth-utils
BuildRequires: python%{python3_pkgversion}-igwn-segments
%endif

%description
DQSEGDB2 is a simplified Python implementation of the DQSEGDB API as defined in
LIGO-T1300625.
This package only provides a query interface for `GET` requests, any users
wishing to make `POST` requests should refer to the official `dqsegdb` Python
client available from https://github.com/ligovirgo/dqsegdb/.

# -- python3x-dqsegdb2

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  Simplified Python %{python3_version} interface to DQSEGDB
Requires: python%{python3_pkgversion} >= 3.6
Requires: python%{python3_pkgversion}-click >= 6.7
Requires: python%{python3_pkgversion}-igwn-auth-utils >= 1.0.0
Requires: python%{python3_pkgversion}-igwn-segments >= 2.0.0
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
DQSEGDB2 is a simplified Python implementation of the DQSEGDB API as defined in
LIGO-T1300625.
This package only provides a query interface for `GET` requests, any users
wishing to make `POST` requests should refer to the official `dqsegdb` Python
client available from https://github.com/ligovirgo/dqsegdb/.

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- dqsegdb2

%package -n dqsegdb2
Summary: Command line utilities for DQSEGDB2
Requires: python%{python3_pkgversion}-%{srcname} = %{version}-%{release}
%description -n dqsegdb2
DQSEGDB2 is a simplified Python implementation of the DQSEGDB API as defined in
LIGO-T1300625.
This package provides the minimal command-line interface.

%files -n dqsegdb2
%doc README.md
%license LICENSE
%{_bindir}/dqsegdb2*
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
%{_mandir}/man*/dqsegdb2*
%endif

# -- build steps

%prep
%autosetup -n %{distname}-%{version}

%if 0%{?rhel} && 0%{?rhel} < 10
echo "Writing setup.cfg for setuptools %{setuptools_version}"
# hack together setup.cfg for old setuptools to parse
cat > setup.cfg << SETUP_CFG
[metadata]
name = %{srcname}
version = %{version}
author-email = %{packager}
description = %{summary}
license = %{license}
license_files = LICENSE
url = %{url}
[options]
packages = find:
python_requires = >=3.6
install_requires =
	igwn-auth-utils >= 1.0.0
	igwn-segments >= 2.0.0
[options.entry_points]
console_scripts =
	dqsegdb2 = dqsegdb2.cli:cli
SETUP_CFG
%endif

%if %{undefined pyproject_wheel}
echo "Writing setup.py for py3_build_wheel"
# write a setup.py to be called explicitly
cat > setup.py << SETUP_PY
from setuptools import setup
setup(use_scm_version=True)
SETUP_PY
%endif

%build
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
%pyproject_wheel
%else
%py3_build_wheel
%endif
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
# generate manuals
%__python3 -c "from setuptools import setup; setup()" \
  --command-packages=click_man.commands \
  man_pages \
  --target man/
%endif

%install
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
%pyproject_install
%else
%py3_install_wheel %{srcname}-%{version}-*.whl
%endif
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
# install manuals
%__mkdir -p -v %{buildroot}%{_mandir}/man1
%__install -m 644 -p -v man/*.1 %{buildroot}%{_mandir}/man1/
%endif

%check
PYTHONPATH="%{buildroot}%{python3_sitelib}" \
%{__python3} -m pip show %{srcname} -f

# -- changelog

%changelog
* Wed Jan 08 2025 Duncan Macleod <duncan.macleod@ligo.org> - 1.3.0-1
- update for 1.3.0
- add Prefix metadata
- specify distname for pypi_source (sdist naming convention changed)
- hack build to create setup.cfg on-the-fly for old setuptools (EL<10)
- add command-line package 'dqsegdb2' with python3-click dependency
- migrate dependency from ligo-segments to igwn-segments

* Fri Aug 25 2023 Duncan Macleod <duncan.macleod@ligo.org> - 1.2.1-1
- update for 1.2.1
- update igwn-auth-utils minimum requirement

* Wed Aug 16 2023 Duncan Macleod <duncan.macleod@ligo.org> - 1.2.0-1
- update for 1.2.0
- update igwn-auth-utils minimum requirement

* Tue May 23 2023 Duncan Macleod <duncan.macleod@ligo.org> - 1.1.4-1
- update for 1.1.4

* Mon Sep 26 2022 Duncan Macleod <duncan.macleod@ligo.org> - 1.1.3-1
- update for 1.1.3
- update igwn-auth-utils requirement
- remove extra Requires for igwn-auth-utils[requests]

* Thu May 05 2022 Duncan Macleod <duncan.macleod@ligo.org> - 1.1.2-1
- update packaging for 1.1.2, reinstates RPM packages
- remove python2 packages
- don't run pytest during build

* Thu Feb 07 2019 Duncan Macleod <duncan.macleod@ligo.org> - 1.0.1-1
- first release
