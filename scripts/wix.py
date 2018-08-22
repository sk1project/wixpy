#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   WiX MSI builder script
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

import json
import os
import sys

import wixpy

HELP_TEMPLATE = '''
%s %s

Crossplatform MSI builder
Copyright (C) 2018 sK1 Project Team (https://wix.sk1project.net)

Usage: wix.py [OPTIONS] [INPUT FILE]
Example: wix.py drawing.json

 Available options:
 --help                Display this help and exit
 --xml_only            Generate WXS representation of MSI package
 --stdout              Show generated WXS representation
 --output=FILE         Resulted MSI/WXS filename
 --xml_encoding=ENC    WXS content encoding (utf-8, cp1251 etc.). Default utf-8
'''

if '--help' in sys.argv or '-help' in sys.argv or len(sys.argv) == 1:
    print(HELP_TEMPLATE % (wixpy.PROJECT, wixpy.VERSION))
    sys.exit(0)

options = [item for item in sys.argv if item.startswith('--')]
non_options = [item for item in sys.argv if not item.startswith('-')]

args = {}
for item in options:
    if '=' in item:
        key, value = item[2:].split('=')[:2]
        if value.lower() in ('yes', 'true'):
            value = True
        if value.lower() in ('no', 'false'):
            value = False
        args[key] = value
    else:
        key = item[2:]
        args[key] = True

if not non_options:
    print('Input JSON file is not provided!')
    sys.exit(1)

json_file = non_options[0]
if not os.path.exists(json_file):
    print('Defined JSON file "%s" is not found!' % json_file)
    sys.exit(1)

json_data = {}
try:
    with open(json_file, 'rb') as fp:
        json_data = json.load(fp)
    if not json_data:
        raise Exception('Empty JSON data!')
except Exception as e:
    print('Error reading JSON file! %s' % str(e))
    sys.exit(1)

wixpy.build(json_data,
            output=args.get('output'),
            stdout=args.get('stdout', False),
            xml_only=args.get('xml_only', False),
            xml_encoding=args.get('xml_encoding', 'utf-8'))
