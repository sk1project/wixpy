# -*- coding: utf-8 -*-
#
#   WiX.Py DEB build script (Ubuntu 16.04 under sudo)
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
import sys

sys.path.insert(0, 'src')

from utils import build, dist
from utils.deb import DebBuilder
import wixpy
import dependencies

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
scripts = ['scripts/py2/wix.py']

targets = [('_ubuntu_16.04', dist.UBUNTU16),
           ('_ubuntu_18.04', dist.UBUNTU18),
           ('_mint_18', dist.MINT18),
           ('_mint_19', dist.MINT19),
           ('_debian_9', dist.DEBIAN9)]

os.system('python setup.py build')
build.compile_sources()

for dist, dist_key in targets:
    deb_depends = ', '.join(dependencies.WIXPY_DEB_PY2[dist_key])
    DebBuilder(
        name=wixpy.PROJECT.lower(),
        version=wixpy.VERSION,
        arch='noarch',
        dist=dist,
        maintainer='%s <%s>' % (wixpy.AUTHOR, wixpy.AUTHOR_EMAIL),
        depends=deb_depends,
        homepage=wixpy.URL,
        description=wixpy.DESCRIPTION,
        long_description=wixpy.LONG_DEB_DESCRIPTION,
        section='devel',
        package_dirs={'wixpy': 'src/wixpy'},
        scripts=scripts,
    )

os.chdir(CURRENT_PATH)
build.clear_build()
