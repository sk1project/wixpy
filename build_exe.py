# -*- coding: utf-8 -*-
#
#   wix.py.exe build script
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

import sys

sys.path.insert(0, 'src')

from distutils.core import setup
import py2exe
import wixpy

INCLUDES = ['os', 'sys']
SCRIPT = "scripts\\wix.py"

setup(
    options={'py2exe': {'bundle_files': 2,
                        'compressed': True,
                        'includes': INCLUDES,
    }},
    console=[{'script': SCRIPT,
              'icon_resources': [(0, 'resources\\wixpy.ico')]
    }],
    zipfile=None,
    name=wixpy.PROJECT,
    version=wixpy.VERSION,
    description="Crossplatform MSI builder",
)