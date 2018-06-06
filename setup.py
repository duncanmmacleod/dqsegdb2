# DQSEGDB2
# Copyright (C) 2018  Duncan Macleod
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Install script for DQSEGDB2
"""

import os
import re

from setuptools import (setup, find_packages)


def parse_version(path):
    """Extract the `__version__` string from the given file
    """
    with open(path, 'r') as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# read description
with open('README.rst', 'rb') as f:
    longdesc = f.read().decode().strip()

setup(
    name='dqsegdb2',
    version=parse_version(os.path.join('dqsegdb2', '__init__.py')),
    author='Duncan Macleod',
    author_email='duncan.macleod@ligo.org',
    description='Simplified python interface to DQSEGDB',
    long_description=longdesc,
    packages=find_packages(),
    setup_requires=['setuptools'],
    install_requires=['six', 'pyOpenSSL'],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Windows',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
