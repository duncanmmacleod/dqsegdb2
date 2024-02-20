%define srcname dqsegdb2
%define version 1.2.1
%define release 1

Name:     python-%{srcname}
Version:  %{version}
Release:  %{release}%{?dist}
Summary:  Simplified python interface to DQSEGDB

License:  GPLv3
Url:      https://pypi.org/project/%{srcname}/
Source0:  %pypi_source

Packager: Duncan Macleod <duncan.macleod@ligo.org>
Vendor:   Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch

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

%description
DQSEGDB2 is a simplified Python implementation of the DQSEGDB API as defined in
LIGO-T1300625.
This package only provides a query interface for `GET` requests, any users
wishing to make `POST` requests should refer to the official `dqsegdb` Python
client available from https://github.com/ligovirgo/dqsegdb/.

# -- python3x-gwdatafind

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  Simplified Python %{python3_version} interface to DQSEGDB
Requires: python%{python3_pkgversion} >= 3.6
Requires: python%{python3_pkgversion}-igwn-auth-utils >= 1.0.0
Requires: python%{python3_pkgversion}-ligo-segments >= 1.0.0
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
DQSEGDB2 is a simplified Python implementation of the DQSEGDB API as defined in
LIGO-T1300625.
This package only provides a query interface for `GET` requests, any users
wishing to make `POST` requests should refer to the official `dqsegdb` Python
client available from https://github.com/ligovirgo/dqsegdb/.

# -- build steps

%prep
%autosetup -n %{srcname}-%{version}
# for RHEL < 9 hack together setup.{cfg,py} for old setuptools
%if 0%{?rhel} > 0 || 0%{?rhel} < 9
cat > setup.cfg <<EOF
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
	ligo-segments >= 1.0.0
EOF
cat > setup.py <<EOF
from setuptools import setup
setup(use_scm_version=True)
EOF
%endif

%build
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
%pyproject_wheel
%else
%py3_build_wheel
%endif

%install
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
%pyproject_install
%else
%py3_install_wheel %{srcname}-%{version}-*.whl
%endif

%check
PYTHONPATH="%{buildroot}%{python3_sitelib}" \
%{__python3} -m pip show %{srcname} -f

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- changelog

%changelog
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
