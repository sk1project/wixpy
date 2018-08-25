# -*- coding: utf-8 -*-
#
#   WiX.Py MSI build script
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
import shutil
from zipfile import ZipFile

sys.path.insert(0, 'src')

from utils import build
from utils.fsutils import get_files_tree
import wixpy


def clear_files(folder, ext=None):
    ext = 'py' if ext is None else ext
    exts = [ext] if not isinstance(ext, list) else ext
    for ext in exts:
        for path in get_files_tree(folder, ext):
            if os.path.exists(path) and path.endswith(ext):
                os.remove(path)


projdir = os.path.dirname(os.path.abspath(__file__))
wixpy_path = os.path.join(projdir, 'src', 'wixpy')
app_icon = os.path.join(projdir, 'resources', 'wixpy.ico')
distro_folder = os.path.join(projdir, 'dist')
if not os.path.exists(distro_folder):
    os.makedirs(distro_folder)

for arch in ('win32', 'win64'):
    print('Init %s build' % arch)
    builddir = os.path.join(projdir, 'build')
    if os.path.exists(builddir):
        shutil.rmtree(builddir, True)
    os.makedirs(builddir)

    print('Extract stdlib')
    portable = os.path.join(projdir, 'resources', 'stdlib-py27-%s.zip' % arch)
    ZipFile(portable, 'r').extractall(builddir)

    for folder in ['stdlib/test/', 'stdlib/lib2to3/tests/']:
        shutil.rmtree(os.path.join(builddir, folder), True)

    print('Copy sources')
    dest = os.path.join(builddir, 'wixpy')
    shutil.copytree(wixpy_path, dest)
    exe_src = os.path.join(projdir, 'scripts', arch, 'wix.py.exe')
    shutil.copy(exe_src, builddir)

    print('Compile sources')
    build.compile_sources(builddir)
    clear_files(builddir, ['py', 'pyo'])

    print('Build MSI')
    win64 = arch == 'win64'
    MSI_DATA = {
        # Required
        'Name': wixpy.PROJECT,
        'UpgradeCode': '3AC4B4FF-10C4-4B8F-81AD-BAC3238BF690',
        'Version': wixpy.VERSION,
        'Manufacturer': 'sK1 Project',
        # Optional
        'Description': '%s %s Installer' % (wixpy.PROJECT, wixpy.VERSION),
        'Comments': 'Licensed under GPLv3',
        'Keywords': 'msi, wix, build',
        'Win64': win64,
        'Codepage': '1252',
        'SummaryCodepage': '1252',
        'Language': '1033',
        'Languages': '1033',

        # Installation features
        '_OsCondition': '601',
        '_CheckX64': win64,
        '_AppIcon': app_icon,
        '_AddToPath': ['', ],
        '_SourceDir': builddir,
        '_InstallDir': 'wixpy-%s' % wixpy.VERSION,
        '_OutputName': '%s-%s-%s.msi' % (wixpy.PROJECT.lower(),
                                         wixpy.VERSION, arch),
        '_OutputDir': distro_folder,
        '_SkipHidden': True,
    }
    wixpy.build(MSI_DATA)
    shutil.rmtree(builddir, True)
