# -*- coding: utf-8 -*-
#
#   wixl related utils
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
import time
import uuid


def get_guid():
    return str(uuid.uuid4()).upper()


def get_id(prefix=''):
    return '%s%s' % (prefix, get_guid().replace('-', ''))


STDOUT_ENDC = '\033[0m'


def echo_msg(msg, newline=True, flush=True, code=''):
    if newline:
        msg += '\n'
    if code:
        msg = code + msg + STDOUT_ENDC
    sys.stdout.write(msg)
    if flush:
        sys.stdout.flush()


DEFAULT_ENCODING = 'utf-8'
MSI_ENCODING = 'cp1252'


def msi_str(text):
    return text.decode(DEFAULT_ENCODING).encode(MSI_ENCODING)


def sql_str(text):
    return msi_str(text.replace("'", "\\'"))


def filetime_now():
    return (int(time.time()) + 134774 * 86400) * 10 ** 7
