# -*- coding: utf-8 -*-
#
#   MSI tables
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

MT_PROPERTY = 'Property'
MT_ICON = 'Icon'
MT_BINARY = 'Binary'
MT_MEDIA = 'Media'
MT_DIRECTORY = 'Directory'
MT_COMPONENT = 'Component'
MT_FEATURE = 'Feature'
MT_FEATURECOMPONENTS = 'FeatureComponents'
MT_REMOVEFILE = 'RemoveFile'
MT_REGISTRY = 'Registry'
MT_SERVICECONTROL = 'ServiceControl'
MT_SERVICEINSTALL = 'ServiceInstall'
MT_FILE = 'File'
MT_ADMINEXECUTESEQUENCE = 'AdminExecuteSequence'
MT_ADMINUISEQUENCE = 'AdminUISequence'
MT_ADVTEXECUTESEQUENCE = 'AdvtExecuteSequence'
MT_INSTALLEXECUTESEQUENCE = 'InstallExecuteSequence'
MT_INSTALLUISEQUENCE = 'InstallUISequence'
MT_STREAMS = '_Streams'
MT_SHORTCUT = 'Shortcut'
MT_UPGRADE = 'Upgrade'
MT_LAUNCHCONDITION = 'LaunchCondition'
MT_APPSEARCH = 'AppSearch'
MT_CUSTOMACTION = 'CustomAction'
MT_REGLOCATOR = 'RegLocator'
MT_CREATEFOLDER = 'CreateFolder'
MT_SIGNATURE = 'Signature'
MT_FILEHASH = 'MsiFileHash'

MT_TABLES = {
    MT_PROPERTY: (
        ('Property', 'CHAR(72) NOT NULL'),
        ('Value', 'CHAR(0) NOT NULL LOCALIZABLE PRIMARY KEY `Property`'),
    ),
    MT_ICON: (
        ('', ''),
    ),  #
    MT_BINARY: (
        ('', ''),
    ),  #
    MT_MEDIA: (
        ('', ''),
    ),  #
    MT_DIRECTORY: (
        ('', ''),
    ),  #
    MT_COMPONENT: (
        ('', ''),
    ),  #
    MT_FEATURE: (
        ('', ''),
    ),  #
    MT_FEATURECOMPONENTS: (
        ('', ''),
    ),  #
    MT_REMOVEFILE: (
        ('', ''),
    ),  #
    MT_REGISTRY: (
        ('', ''),
    ),  #
    MT_SERVICECONTROL: (
        ('', ''),
    ),  #
    MT_SERVICEINSTALL: (
        ('', ''),
    ),  #
    MT_FILE: (
        ('', ''),
    ),  #
    MT_ADMINEXECUTESEQUENCE: (
        ('', ''),
    ),  #
    MT_ADMINUISEQUENCE: (
        ('', ''),
    ),  #
    MT_ADVTEXECUTESEQUENCE: (
        ('', ''),
    ),  #
    MT_INSTALLEXECUTESEQUENCE: (
        ('', ''),
    ),  #
    MT_INSTALLUISEQUENCE: (
        ('', ''),
    ),  #
    MT_STREAMS: (
        ('', ''),
    ),  #
    MT_SHORTCUT: (
        ('', ''),
    ),  #
    MT_UPGRADE: (
        ('', ''),
    ),  #
    MT_LAUNCHCONDITION: (
        ('', ''),
    ),  #
    MT_APPSEARCH: (
        ('', ''),
    ),  #
    MT_CUSTOMACTION: (
        ('', ''),
    ),  #
    MT_REGLOCATOR: (
        ('', ''),
    ),  #
    MT_CREATEFOLDER: (
        ('', ''),
    ),  #
    MT_SIGNATURE: (
        ('', ''),
    ),  #
    MT_FILEHASH: (
        ('', ''),
    ),  #
}
