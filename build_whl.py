# -*- coding: utf-8 -*-
#
#   WiX.Py WHL build
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
import setuptools
import sys

sys.path.insert(1, os.path.abspath('./src'))

import wixpy

if 'bdist_wheel' not in sys.argv:
    sys.argv.append('bdist_wheel')

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name=wixpy.PROJECT,
    version=wixpy.VERSION,
    author=wixpy.AUTHOR,
    author_email=wixpy.AUTHOR_EMAIL,
    description=wixpy.DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://wix.sk1project.net',
    packages=['wixpy'],
    package_dir={'wixpy': 'src/wixpy'},
    classifiers=wixpy.CLASSIFIERS,
    scripts=['scripts/wix.py'],
    python_requires='>=2.7, <3',
    keywords='wix msi',
)
