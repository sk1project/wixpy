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
Supported features:
* JSON-driven MSI generation
* recursive app folder scanning
* msi package icon
* 32/64bit installations
* ProgramMenu folder and shortcuts
* OS version check
* x64 arch check
* custom conditions
* add to system PATH

Planned features:
* Crossplatform MSI-generation backend
* File type associations (Open, Open with)
* MIME-type for files
* Open port
* GUI for compiled msi-installers
"""

import os
import shutil
import sys

from wixpy import model
from wixpy import utils

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
        if os.name == 'nt':
            raise Exception('WiX.py backend is not supported on Windows yet!')
        from wixpy import libmsi, msi
        msi.MSI_CODEPAGE = wixmodel.get_package().get('SummaryCodepage')
        utils.echo_msg('Writing MSI package into %s...' % output)
        libmsi.MsiDatabase(wixmodel).write_msi(output)

    wixmodel.destroy()


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(current_path)
    projdir = os.path.dirname(path)
    app_icon = os.path.join(projdir, 'resources', 'wixpy.ico')

    # Prepare build dir
    builddir = os.path.join(projdir, 'build')
    if os.path.exists(builddir):
        shutil.rmtree(builddir, True)
    os.makedirs(builddir)
    dest = os.path.join(builddir, os.path.basename(current_path))
    shutil.copytree(current_path, dest)
    exe_src = os.path.join(projdir, 'scripts', 'wix.py.exe')
    shutil.copy(exe_src, builddir)

    # MSI build data
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
        'Codepage': '1251',
        'SummaryCodepage': '1251',
        'Language': '1049',  # 1033
        'Languages': '1049',

        # Installation infrastructure
        '_OsCondition': 601,
        '_CheckX64': win64,
        '_Conditions': [],  # [[msg,condition,level], ...]
        '_AppIcon': app_icon,
        '_Icons': [],
        '_ProgramMenuFolder': 'sK1 Project',
        '_Shortcuts': [
            {'Name': PROJECT,
             'Description': 'Crossplatform MSI builder',
             'Target': 'wix.py.exe',
             'Open': [],
             'OpenWith': [],
             'EditWith': [],
             },
        ],
        '_AddToPath': ['', ],
        '_AddBeforePath': [],
        '_SourceDir': builddir,
        '_InstallDir': 'wixpy-%s' % VERSION,
        '_OutputName': '%s-%s-%s.msi' % (PROJECT.lower(), VERSION,
                                         'win64' if win64 else 'win32'),
        '_OutputDir': '~',
        '_SkipHidden': True,
    }

    # MSI build
    try:
        # build(MSI_DATA, xml_only=True, engine=Engine.WIXL, stdout=True)
        build(MSI_DATA, xml_only=True, stdout=True)
        # build(MSI_DATA)
    except Exception as e:
        raise e
    finally:
        shutil.rmtree(builddir, True)
