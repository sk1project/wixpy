# -*- coding: utf-8 -*-
#
#   WiX related utils
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

import hashlib
import struct
import sys
import time
import uuid

IS_PY3 = sys.version_info.major > 2


def get_guid():
    return str(uuid.uuid4()).upper()


def get_id(prefix=''):
    return '%s%s' % (prefix, get_guid().replace('-', ''))


STDOUT_ENDC = '\033[0m'


def echo_msg(msg, newline=True, flush=True, code=''):
    msg += '\n' if newline else ''
    msg = code + msg + STDOUT_ENDC if code else msg
    sys.stdout.write(msg)
    sys.stdout.flush() if flush else None


def filetime_now():
    return (int(time.time()) + 134774 * 86400) * 10 ** 7


def compute_md5(filepath):
    with open(filepath, 'rb') as fp:
        hash = hashlib.md5(fp.read()).hexdigest()
        data = bytes.fromhex(hash) if IS_PY3 else hash.decode('hex')
    return struct.unpack('<iiii', data)


XML_ENCODING = 'utf-8'


class XmlWriter(object):
    fp = None

    def __init__(self, filepointer):
        self.fp = filepointer

    def write(self, text):
        if IS_PY3:
            text = text.encode(XML_ENCODING, errors='replace')
        elif XML_ENCODING != 'utf-8':
            text = text.decode('utf-8').encode(XML_ENCODING, errors='replace')
        self.fp.write(text)
