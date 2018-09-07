# -*- coding: utf-8 -*-
#
#   Cross-platform MSI builder
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

"""
Supported features:
* Cross-platform MSI-generation
* JSON-driven MSI build
* Recursive app folder scanning
* Localizable installer
* MSI package icon
* 32/64bit installations
* ProgramMenu folder and shortcuts
* Desktop shortcuts
* OS version check
* x64 arch check
* Custom conditions
* Add to system PATH
* File type associations (Open, Open with)
* MIME-type and icon for associated files
* 'Edit with' menu item for associated files

Planned features:
* GUI for compiled MSI installers
"""

import datetime
import os
import sys

from wixpy import model
from wixpy import utils

PROJECT = 'WiX.Py'
VERSION = '0.1'
UPGRADE_CODE = '3AC4B4FF-10C4-4B8F-81AD-BAC3238BF690'
DESCRIPTION = 'Cross-platform MSI builder'
AUTHOR = 'Igor E. Novikov'
AUTHOR_EMAIL = 'sk1.project.org@gmail.com'
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
MANUFACTURER = 'sK1 Project'
LICENSE = 'GPL v3'
URL = 'https://wix.sk1project.net'
DOWNLOAD_URL = URL
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 2.7',
    "Topic :: Software Development :: Build Tools",
]
LONG_DESCRIPTION = '''
WiX.Py is an open source cross-platform alternative for WiX toolset.
Application allows building MSI packages as under MSW and Linux
platforms including inside Docker environment. Unlike WiX/wixl applications
WiX.Py is an JSON-driven builder. To build MSI package you need filling
small JSON file only, describing generic application data (name, version etc.)

Copyright (C) %s sK1 Project Team (https://wix.sk1project.net)
''' % str(datetime.date.today().year)

LONG_DEB_DESCRIPTION = ''' .
 WiX.Py is an open source cross-platform alternative for WiX toolset.
 Application allows building MSI packages as under MSW and Linux
 platforms including inside Docker environment. Unlike WiX/wixl applications
 WiX.Py is an JSON-driven builder. To build MSI package you need filling
 small JSON file only, describing generic application data (name, version etc.)
 .
 Copyright (C) %s sK1 Project Team (https://wix.sk1project.net)
 .
''' % str(datetime.date.today().year)

KEYWORDS = ['msi', 'wix', 'build']


class Engine(object):
    WIXPY = 0
    WIXL = 1
    WIX = 2

    @classmethod
    def from_string(cls, engine_name):
        return {'WIXPY': cls.WIXPY,
                'WIXL': cls.WIXL,
                'WIX': cls.WIX}.get(engine_name.upper(), cls.WIXPY)

    @classmethod
    def to_string(cls, engine):
        return {cls.WIXPY: 'WIXPY',
                cls.WIXL: 'WIXL',
                cls.WIX: 'WIX'}.get(engine, 'WIXPY')

    @classmethod
    def normalize(cls, value):
        if isinstance(value, int):
            return cls.from_string(cls.to_string(value))
        else:
            return cls.to_string(cls.from_string(value))


def _normalize_path(wild_path):
    return os.path.abspath(os.path.expanduser(wild_path))


def _normalize_json_data(json_data):
    json_data['_pkgname'] = PROJECT
    json_data['_pkgver'] = VERSION

    if 'Win64' in json_data:
        if json_data['Win64'] in [True, 'yes']:
            json_data['Win64'] = 'yes'
            json_data['_CheckX64'] = True
        else:
            json_data.pop('Win64')
            json_data['_CheckX64'] = False

    if '_OsCondition' in json_data:
        json_data['_OsCondition'] = str(json_data['_OsCondition'])

    for key in ('_Icon', '_OutputDir', '_SourceDir'):
        if key in json_data:
            json_data[key] = _normalize_path(json_data[key])

    return json_data


def _get_output_path(json_data=None, output=None, xml_only=False, stdout=False):
    filename = ''
    dirpath = _normalize_path('./')

    if output:
        output = _normalize_path(output)
        filename = os.path.basename(output)
        if os.path.dirname(output):
            dirpath = os.path.dirname(output)
    elif json_data and json_data.get('_OutputName'):
        filename = json_data.get('_OutputName')
        if json_data.get('_OutputDir'):
            dirpath = _normalize_path(json_data.get('_OutputDir'))

    if xml_only and stdout:
        return None

    if not filename:
        raise Exception('Output filename is not defined!')

    if not xml_only and not filename.endswith('.msi'):
        filename += '.msi'
    elif xml_only and not filename.endswith('.wxs'):
        filename += '.wxs'

    return os.path.join(dirpath, filename)


def create_model(json_data=None, xml_file=None):
    if json_data:
        return model.Wix(_normalize_json_data(json_data))
    elif xml_file:
        raise Exception('XML loader is not implemented yet')
    else:
        raise Exception('Neither JSON nor XML data have been provided!')


def build(json_data=None, output=None, xml_only=False, xml_encoding=None,
          engine=Engine.WIXPY, stdout=False):
    output = _get_output_path(json_data, output, xml_only, stdout)
    utils.XML_ENCODING = xml_encoding or 'utf-8'

    wixmodel = create_model(json_data)

    if xml_only:
        model.WIXL = engine == Engine.WIXL
        if stdout:
            wixmodel.write_xml(sys.stdout)
        else:
            utils.echo_msg('Writing XML into %s...' % output)
            with open(output, 'wb') as fp:
                wixmodel.write_xml(utils.XmlWriter(fp))
    else:
        from wixpy import msi
        msi.MSI_CODEPAGE = wixmodel.get_package().get('SummaryCodepage')
        utils.echo_msg('Writing MSI package into %s...' % output)
        msi.MsiDatabase(wixmodel).write_msi(output)

        if stdout:
            wixmodel.write_xml(sys.stdout)

    wixmodel.destroy()
