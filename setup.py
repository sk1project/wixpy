# -*- coding: utf-8 -*-
#
#   WiX.Py MSI builder setup
#
#   Copyright (C) 2018 by Igor E. Novikov
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import platform
import sys

from distutils.core import setup

import datetime

sys.path.insert(1, os.path.abspath('./src'))

IS_WIN32 = platform.architecture()[0] == '32bit'
WIN_ARCH = 'win32' if IS_WIN32 else 'win64'
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

import wixpy

NAME = wixpy.PROJECT
VERSION = wixpy.VERSION
DESCRIPTION = 'Crossplatform MSI builder'
AUTHOR = 'Igor E. Novikov'
AUTHOR_EMAIL = 'sk1.project.org@gmail.com'
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = 'GPL v3'
URL = 'https://wix.sk1project.net'
DOWNLOAD_URL = URL
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 2.7',
    "Topic :: Software Development :: Build Tools",
]
LONG_DESCRIPTION = '''
WiX.Py is an open source crossplatform alternative for WiX toolset.
Application allows building MSI packages as under MSW and Linux
platforms including inside Docker environment. Unlike WiX/wixl applications
WiX.Py is an JSON-driven builder. To build MSI package you need filling
small JSON file only, describing generic application data (name, version etc.)

Copyright (C) %s sK1 Project Team (https://wix.sk1project.net)
''' % str(datetime.date.today().year)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    packages=['wixpy'],
    package_dir={'wixpy': 'src/wixpy'},
    scripts=['scripts/%s/wix.py.exe' % WIN_ARCH] if os.name == 'nt'
    else ['scripts/wix.py'],
)