# -*- coding: utf-8 -*-
#
#   MSW MSI builder
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
Supported features (WiX & wixl):
* JSON-driven MSI generation
* recursive app folder scanning
* msi package icon
* 32/64bit installations
* ProgramMenu folder and shortcuts
* OS version check
* x64 arch check
* custom conditions

Planned features:
* GUI for compiled msi-installers
* Extension associations (Open, Open with)
* add to system PATH
"""

import os
import sys
import tempfile

import model
import utils

PROJECT = 'WiX.Py'
VERSION = '0.1'


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


def _normalize_path(wild_path):
    return os.path.abspath(os.path.expanduser(wild_path))


def build(json_data, xml_only=False, engine=Engine.WIXPY,
          encoding='utf-8', stdout=False):
    utils.echo_msg('Starting with %s engine' % Engine.to_string(engine))
    utils.DEFAULT_ENCODING = encoding
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

    output = json_data.get('_OutputName')
    if not output:
        raise Exception('Output filename is not defined!')
    if not xml_only and not output.endswith('.msi'):
        output += '.msi'
    elif xml_only and not output.endswith('.wxs'):
        output += '.wxs'
    output_path = os.path.join(json_data.get('_OutputDir', './'), output)

    model.WIXL = engine == Engine.WIXL

    utils.echo_msg('Building Wix model...')
    wixmodel = model.Wix(json_data)

    if xml_only:
        if stdout:
            wixmodel.write_xml(sys.stdout)
        else:
            utils.echo_msg('Writing XML into %s...' % output_path)
            with open(output_path, 'wb') as fp:
                wixmodel.write_xml(fp)

    elif engine == Engine.WIXL:
        xml_file = tempfile.NamedTemporaryFile(delete=True)
        with open(xml_file.name, 'wb') as fp:
            wixmodel.write_xml(fp)
        arch = '-a x64' if json_data.get('Win64') else ''
        os.system('wixl -v %s -o %s %s' % (arch, output_path, xml_file.name))

    elif engine == Engine.WIX:
        raise Exception('WiX backend support is not implemented yet!')

    elif engine == Engine.WIXPY:
        if os.name == 'nt':
            raise Exception('WiX.py backend is not supported on MS Windows!')
        import libmsi
        utils.echo_msg('Writing MSI package into %s...' % output_path)
        libmsi.MsiDatabase(wixmodel).write_msi(output_path)

    wixmodel.destroy()


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(current_path)
    win64 = True
    MSI_DATA = {
        # Required
        'Name': PROJECT,
        'UpgradeCode': '3AC4B4FF-10C4-4B8F-81AD-BAC3238BF690',
        'Version': VERSION,
        'Manufacturer': 'sK1 Project',
        # Optional
        'Description': '%s %s Installer' % (PROJECT, VERSION),
        'Comments': 'Licensed under GPLv3',
        'Keywords': 'msi, wix, build',
        'Win64': win64,

        # Installation infrastructure
        '_OsCondition': 601,
        '_CheckX64': win64,
        '_Conditions': [],  # [[msg,condition,level], ...]
        '_Icon': '~/Projects/wixpy.ico',
        '_ProgramMenuFolder': 'sK1 Project',
        '_Shortcuts': [
            {'Name': PROJECT,
             'Description': 'Multiplatform MSI builder',
             'Target': '__init__.py'},
        ],
        '_SourceDir': path,
        '_InstallDir': 'wixpy-%s' % VERSION,
        '_OutputName': '%s-%s-%s.msi' % (PROJECT.lower(), VERSION,
                                         'win64' if win64 else 'win32'),
        '_OutputDir': '~',
        '_SkipHidden': True,
    }
    # build(MSI_DATA, xml_only=True, engine=WIXL_ENGINE, stdout=True)
    build(MSI_DATA, xml_only=True, stdout=True)
    # build(MSI_DATA, engine=WIXL_ENGINE)
    # build(MSI_DATA)
