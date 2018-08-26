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

setup(
    name=wixpy.PROJECT,
    version=wixpy.VERSION,
    description=wixpy.DESCRIPTION,
    author=wixpy.AUTHOR,
    author_email=wixpy.AUTHOR_EMAIL,
    maintainer=wixpy.MAINTAINER,
    maintainer_email=wixpy.MAINTAINER_EMAIL,
    license=wixpy.LICENSE,
    url=wixpy.URL,
    download_url=wixpy.DOWNLOAD_URL,
    long_description=wixpy.LONG_DESCRIPTION,
    classifiers=wixpy.CLASSIFIERS,
    packages=['wixpy'],
    package_dir={'wixpy': 'src/wixpy'},
    scripts=['scripts/%s/wix.py.exe' % WIN_ARCH] if os.name == 'nt'
    else ['scripts/wix.py'],
)
