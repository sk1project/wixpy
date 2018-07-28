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

MT_ACTION = (('Action', 'CHAR(72) NOT NULL'),
             ('Condition', 'CHAR(255)'),
             ('Sequence', 'INT PRIMARY KEY `Action`'),)

MT_TABLES = {
    MT_PROPERTY: (
        ('Property', 'CHAR(72) NOT NULL'),
        ('Value', 'CHAR(0) NOT NULL LOCALIZABLE PRIMARY KEY `Property`'),
    ),
    MT_ICON: (
        ('Name', 'CHAR(72) NOT NULL'),
        ('Data', 'OBJECT NOT NULL PRIMARY KEY `Name`'),
    ),
    MT_BINARY: (
        ('Name', 'CHAR(72) NOT NULL'),
        ('Data', 'OBJECT NOT NULL PRIMARY KEY `Name`'),
    ),
    MT_MEDIA: (
        ('DiskId', 'INT NOT NULL'),
        ('LastSequence', 'LONG NOT NULL'),
        ('DiskPrompt', 'CHAR(64) LOCALIZABLE'),
        ('Cabinet', 'CHAR(255)'),
        ('VolumeLabel', 'CHAR(32)'),
        ('Source', 'CHAR(72) PRIMARY KEY `DiskId`'),
    ),
    MT_DIRECTORY: (
        ('Directory', 'CHAR(72) NOT NULL'),
        ('Directory_Parent', 'CHAR(72)'),
        ('DefaultDir', 'CHAR(255) NOT NULL LOCALIZABLE PRIMARY KEY `Directory`')
    ),
    MT_COMPONENT: (
        ('Component', 'CHAR(72) NOT NULL'),
        ('ComponentId', 'CHAR(38)'),
        ('Directory_', 'CHAR(72) NOT NULL'),
        ('Attributes', 'INT NOT NULL'),
        ('Condition', 'CHAR(255)'),
        ('KeyPath', 'CHAR(72) PRIMARY KEY `Component`'),
    ),
    MT_FEATURE: (
        ('Feature', 'CHAR(38) NOT NULL'),
        ('Feature_Parent', 'CHAR(38)'),
        ('Title', 'CHAR(64) LOCALIZABLE'),
        ('Description', 'CHAR(255) LOCALIZABLE'),
        ('Display', 'INT'),
        ('Level', 'INT NOT NULL'),
        ('Directory_', 'CHAR(72)'),
        ('Attributes', 'INT NOT NULL PRIMARY KEY `Feature`')
    ),
    MT_FEATURECOMPONENTS: (
        ('Feature_', 'CHAR(38) NOT NULL'),
        ('Component_', 'CHAR(72) NOT NULL PRIMARY KEY `Feature_`, `Component_`')
    ),
    MT_REMOVEFILE: (
        ('FileKey', 'CHAR(72) NOT NULL'),
        ('Component_', 'CHAR(72) NOT NULL'),
        ('FileName', 'CHAR(255) LOCALIZABLE'),
        ('DirProperty', 'CHAR(72) NOT NULL'),
        ('InstallMode', 'INT NOT NULL PRIMARY KEY `FileKey`'),
    ),
    MT_REGISTRY: (
        ('Registry', 'CHAR(72) NOT NULL'),
        ('Root', 'INT NOT NULL'),
        ('Key', 'CHAR(255) NOT NULL LOCALIZABLE'),
        ('Name', 'CHAR(255) LOCALIZABLE'),
        ('Value', 'CHAR(0) LOCALIZABLE'),
        ('Component_', 'CHAR(72) NOT NULL PRIMARY KEY `Registry`'),
    ),
    MT_SERVICECONTROL: (
        ('ServiceControl', 'CHAR(72) NOT NULL'),
        ('Name', 'CHAR(255) NOT NULL LOCALIZABLE'),
        ('Event', 'INT NOT NULL'),
        ('Arguments', 'CHAR(255) LOCALIZABLE'),
        ('Wait', 'INT'),
        ('Component_', 'CHAR(72) NOT NULL PRIMARY KEY `ServiceControl`'),
    ),
    MT_SERVICEINSTALL: (
        ('ServiceInstall', 'CHAR(72) NOT NULL'),
        ('Name', 'CHAR(255) NOT NULL'),
        ('DisplayName', 'CHAR(255) LOCALIZABLE'),
        ('ServiceType', 'LONG NOT NULL'),
        ('StartType', 'LONG NOT NULL'),
        ('ErrorControl', 'LONG NOT NULL'),
        ('LoadOrderGroup', 'CHAR(255)'),
        ('Dependencies', 'CHAR(255)'),
        ('StartName', 'CHAR(255)'),
        ('Password', 'CHAR(255)'),
        ('Arguments', 'CHAR(255)'),
        ('Component_', 'CHAR(72) NOT NULL'),
        ('Description', 'CHAR(255) LOCALIZABLE PRIMARY KEY `ServiceInstall`'),
    ),
    MT_FILE: (
        ('File', 'CHAR(72) NOT NULL'),
        ('Component_', 'CHAR(72) NOT NULL'),
        ('FileName', 'CHAR(255) NOT NULL LOCALIZABLE'),
        ('FileSize', 'LONG NOT NULL'),
        ('Version', 'CHAR(72)'),
        ('Language', 'CHAR(20)'),
        ('Attributes', 'INT'),
        ('Sequence', 'LONG NOT NULL PRIMARY KEY `File`'),
    ),
    MT_ADMINEXECUTESEQUENCE: MT_ACTION,
    MT_ADMINUISEQUENCE: MT_ACTION,
    MT_ADVTEXECUTESEQUENCE: MT_ACTION,
    MT_INSTALLEXECUTESEQUENCE: MT_ACTION,
    MT_INSTALLUISEQUENCE: MT_ACTION,
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
