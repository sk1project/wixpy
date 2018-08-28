# -*- coding: utf-8 -*-
#
#   WiX.Py dependencies resolver
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

from utils.dist import *

IS_PY2 = sys.version_info.major < 3
IS_MSW = os.name == 'nt'

WIXPY_DEB_PY2 = {
    UBUNTU16: ['python-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi0',
               'gir1.2-libgcab-1.0'],
    UBUNTU17: ['python-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi-1.0',
               'gir1.2-gcab-1.0'],
    UBUNTU18: ['python-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi-1.0',
               'gir1.2-gcab-1.0'],
    MINT18: ['python-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi0',
             'gir1.2-libgcab-1.0'],
    MINT19: ['python-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi-1.0',
             'gir1.2-gcab-1.0'],
    DEBIAN9: ['python-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi0',
              'gir1.2-libgcab-1.0'],
}

WIXPY_DEB_PY3 = {
    UBUNTU16: ['python3-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi0',
               'gir1.2-libgcab-1.0'],
    UBUNTU17: ['python3-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi-1.0',
               'gir1.2-gcab-1.0'],
    UBUNTU18: ['python3-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi-1.0',
               'gir1.2-gcab-1.0'],
    MINT18: ['python3-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi0',
             'gir1.2-libgcab-1.0'],
    MINT19: ['python3-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi-1.0',
             'gir1.2-gcab-1.0'],
    DEBIAN9: ['python3-gi', 'gir1.2-glib-2.0', 'gir1.2-libmsi0',
              'gir1.2-libgcab-1.0'],
}

WIXPY_RPM_PY2 = {
    FEDORA26: ['python-gobject-base', 'gobject-introspection', 'libmsi1',
               'libgcab1'],
    FEDORA27: ['python2-gobject-base', 'gobject-introspection', 'libmsi1',
               'libgcab1'],
    FEDORA28: ['python2-gobject-base', 'gobject-introspection', 'libmsi1',
               'libgcab1'],
    OPENSUSE15_0: ['python2-gobject', 'girepository-1_0',
                   'typelib-1_0-Libmsi-1_0', 'typelib-1_0-GCab-1_0'],
}
WIXPY_RPM_PY3 = {
    FEDORA26: ['python3-gobject-base', 'gobject-introspection', 'libmsi1',
               'libgcab1'],
    FEDORA27: ['python3-gobject-base', 'gobject-introspection', 'libmsi1',
               'libgcab1'],
    FEDORA28: ['python3-gobject-base', 'gobject-introspection', 'libmsi1',
               'libgcab1'],
    OPENSUSE15_0: ['python3-gobject', 'girepository-1_0',
                   'typelib-1_0-Libmsi-1_0', 'typelib-1_0-GCab-1_0'],
}

WARNING = '''

WARNING!
--------
Dependencies for you distributive are unknown. Please install manually following
packages: python-gi, gir1.2-glib, gir1.2-libmsi, gir1.2-libgcab
May be they have different names in your system. Take a look at dependencies.py
file for hints.

'''


def install():
    installed = IS_MSW
    if not installed:
        if SYSFACTS.is_deb:
            deps_dict = WIXPY_DEB_PY2 if IS_PY2 else WIXPY_DEB_PY3
            deps = ' '.join(deps_dict.get(SYSFACTS.sid, []))
            if deps:
                os.system('sudo apt-get -y install %s' % deps)
                installed = True
        elif SYSFACTS.is_rpm:
            deps_dict = WIXPY_RPM_PY2 if IS_PY2 else WIXPY_RPM_PY3
            deps = ' '.join(deps_dict.get(SYSFACTS.sid, []))
            if deps:
                os.system('yum -y install %s' % deps)
                installed = True
    if not installed:
        print(WARNING)
