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
    UBUNTU16: ['python-gi', 'gir1.2-glib-2.0',
               'gir1.2-libmsi0', 'gir1.2-libgcab-1.0'],
}

WIXPY_RPM = {}


def install():
    if not IS_MSW and IS_PY2:
        if SYSFACTS.is_deb and SYSFACTS.sid in WIXPY_DEB_PY2:
            deps = ' '.join(WIXPY_DEB_PY2[SYSFACTS.sid])
            os.system('sudo apt-get -y install %s' % deps)
    elif not IS_MSW and not IS_PY2:
        pass
