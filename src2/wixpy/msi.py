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

# ----------- MSI enums -----------


class SourceFlags(object):
    SHORT_NAMES = 1
    COMPRESSED = 2
    ADMIN = 4
    NO_PRIVILEGES = 8


class ComponentAttribute(object):
    LOCAL_ONLY = 0
    SOURCE_ONLY = 1
    OPTIONAL = 2
    REGISTRY_KEY_PATH = 4
    SHARED_DLL_REF_COUNT = 8
    PERMANENT = 16
    ODBC_DATA_SOURCE = 32
    TRANSITIVE = 64
    NEVER_OVERWRITE = 128
    X64 = 256
    REGISTRY_REFLECTION = 512
    UNINSTALL_ON_SUPERSEDENCE = 1024
    SHARED = 2048


class FeatureDisplay(object):
    HIDDEN = 0
    EXPAND = 1
    COLLAPSE = 2


class InstallMode(object):
    INSTALL = 1
    UNINSTALL = 2
    BOTH = 4

    @classmethod
    def from_string(cls, str_value):
        return {'install': cls.INSTALL,
                'uninstall': cls.UNINSTALL,
                'both': cls.BOTH}[str_value]


class RegistryValueType(object):
    STRING = 1
    INTEGER = 2
    BINARY = 4
    EXPANDABLE = 8
    MULTI_STRING = 16

    @classmethod
    def from_string(cls, str_value):
        return {'string': cls.STRING,
                'integer': cls.INTEGER,
                'binary': cls.BINARY,
                'expandable': cls.EXPANDABLE,
                'multistring': cls.MULTI_STRING}[str_value]


class RegistryRoot(object):
    HKCR = 1
    HKCU = 2
    HKLM = 4
    HKU = 8
    HKMU = 16

    @classmethod
    def from_string(cls, str_value):
        return {'HKCR': cls.HKCR,
                'HKCU': cls.HKCU,
                'HKLM': cls.HKLM,
                'HKU': cls.HKU,
                'HKMU': cls.HKMU}[str_value]


# ----------- MSI Tables -----------

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
             ('Sequence', 'INT '
                          'PRIMARY KEY `Action`'),)

MT_TABLES = {
    MT_PROPERTY: (
        ('Property', 'CHAR(72) NOT NULL'),
        ('Value', 'CHAR(0) NOT NULL LOCALIZABLE '
                  'PRIMARY KEY `Property`'),
    ),
    MT_ICON: (
        ('Name', 'CHAR(72) NOT NULL'),
        ('Data', 'OBJECT NOT NULL '
                 'PRIMARY KEY `Name`'),
    ),
    MT_BINARY: (
        ('Name', 'CHAR(72) NOT NULL'),
        ('Data', 'OBJECT NOT NULL '
                 'PRIMARY KEY `Name`'),
    ),
    MT_MEDIA: (
        ('DiskId', 'INT NOT NULL'),
        ('LastSequence', 'LONG NOT NULL'),
        ('DiskPrompt', 'CHAR(64) LOCALIZABLE'),
        ('Cabinet', 'CHAR(255)'),
        ('VolumeLabel', 'CHAR(32)'),
        ('Source', 'CHAR(72) '
                   'PRIMARY KEY `DiskId`'),
    ),
    MT_DIRECTORY: (
        ('Directory', 'CHAR(72) NOT NULL'),
        ('Directory_Parent', 'CHAR(72)'),
        ('DefaultDir', 'CHAR(255) NOT NULL LOCALIZABLE '
                       'PRIMARY KEY `Directory`')
    ),
    MT_COMPONENT: (
        ('Component', 'CHAR(72) NOT NULL'),
        ('ComponentId', 'CHAR(38)'),
        ('Directory_', 'CHAR(72) NOT NULL'),
        ('Attributes', 'INT NOT NULL'),
        ('Condition', 'CHAR(255)'),
        ('KeyPath', 'CHAR(72) '
                    'PRIMARY KEY `Component`'),
    ),
    MT_FEATURE: (
        ('Feature', 'CHAR(38) NOT NULL'),
        ('Feature_Parent', 'CHAR(38)'),
        ('Title', 'CHAR(64) LOCALIZABLE'),
        ('Description', 'CHAR(255) LOCALIZABLE'),
        ('Display', 'INT'),
        ('Level', 'INT NOT NULL'),
        ('Directory_', 'CHAR(72)'),
        ('Attributes', 'INT NOT NULL '
                       'PRIMARY KEY `Feature`')
    ),
    MT_FEATURECOMPONENTS: (
        ('Feature_', 'CHAR(38) NOT NULL'),
        ('Component_', 'CHAR(72) NOT NULL '
                       'PRIMARY KEY `Feature_`, `Component_`')
    ),
    MT_REMOVEFILE: (
        ('FileKey', 'CHAR(72) NOT NULL'),
        ('Component_', 'CHAR(72) NOT NULL'),
        ('FileName', 'CHAR(255) LOCALIZABLE'),
        ('DirProperty', 'CHAR(72) NOT NULL'),
        ('InstallMode', 'INT NOT NULL '
                        'PRIMARY KEY `FileKey`'),
    ),
    MT_REGISTRY: (
        ('Registry', 'CHAR(72) NOT NULL'),
        ('Root', 'INT NOT NULL'),
        ('Key', 'CHAR(255) NOT NULL LOCALIZABLE'),
        ('Name', 'CHAR(255) LOCALIZABLE'),
        ('Value', 'CHAR(255) LOCALIZABLE'),
        ('Component_', 'CHAR(72) NOT NULL PRIMARY KEY `Registry`'),
    ),
    MT_SERVICECONTROL: (
        ('ServiceControl', 'CHAR(72) NOT NULL'),
        ('Name', 'CHAR(255) NOT NULL LOCALIZABLE'),
        ('Event', 'INT NOT NULL'),
        ('Arguments', 'CHAR(255) LOCALIZABLE'),
        ('Wait', 'INT'),
        ('Component_', 'CHAR(72) NOT NULL '
                       'PRIMARY KEY `ServiceControl`'),
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
        ('Description', 'CHAR(255) LOCALIZABLE '
                        'PRIMARY KEY `ServiceInstall`'),
    ),
    MT_FILE: (
        ('File', 'CHAR(72) NOT NULL'),
        ('Component_', 'CHAR(72) NOT NULL'),
        ('FileName', 'CHAR(255) NOT NULL LOCALIZABLE'),
        ('FileSize', 'LONG NOT NULL'),
        ('Version', 'CHAR(72)'),
        ('Language', 'CHAR(20)'),
        ('Attributes', 'INT'),
        ('Sequence', 'LONG NOT NULL '
                     'PRIMARY KEY `File`'),
    ),
    MT_ADMINEXECUTESEQUENCE: MT_ACTION,
    MT_ADMINUISEQUENCE: MT_ACTION,
    MT_ADVTEXECUTESEQUENCE: MT_ACTION,
    MT_INSTALLEXECUTESEQUENCE: MT_ACTION,
    MT_INSTALLUISEQUENCE: MT_ACTION,
    MT_STREAMS: (
        ('Name', 'CHAR(72) NOT NULL'),
        ('Data', 'OBJECT NOT NULL '
                 'PRIMARY KEY `Name`'),
    ),
    MT_SHORTCUT: (
        ('Shortcut', 'CHAR(72) NOT NULL'),
        ('Directory_', 'CHAR(72) NOT NULL'),
        ('Name', 'CHAR(128) NOT NULL LOCALIZABLE'),
        ('Component_', 'CHAR(72) NOT NULL'),
        ('Target', 'CHAR(72) NOT NULL'),
        ('Arguments', 'CHAR(255)'),
        ('Description', 'CHAR(255) LOCALIZABLE'),
        ('Hotkey', 'INT'),
        ('Icon_', 'CHAR(72)'),
        ('IconIndex', 'INT'),
        ('ShowCmd', 'INT'),
        ('WkDir', 'CHAR(72)'),
        ('DisplayResourceDLL', 'CHAR(255)'),
        ('DisplayResourceId', 'INT'),
        ('DescriptionResourceDLL', 'CHAR(255)'),
        ('DescriptionResourceId', 'INT '
                                  'PRIMARY KEY `Shortcut`'),
    ),
    MT_UPGRADE: (
        ('UpgradeCode', 'CHAR(38) NOT NULL'),
        ('VersionMin', 'CHAR(20)'),
        ('VersionMax', 'CHAR(20)'),
        ('Language', 'CHAR(255)'),
        ('Attributes', 'LONG NOT NULL'),
        ('Remove', 'CHAR(255)'),
        ('ActionProperty', 'CHAR(72) NOT NULL '
                           'PRIMARY KEY `UpgradeCode`, `VersionMin`, '
                           '`VersionMax`, `Language`, `Attributes`'),
    ),
    MT_LAUNCHCONDITION: (
        ('Condition', 'CHAR(255) NOT NULL'),
        ('Description', 'CHAR(255) NOT NULL '
                        'LOCALIZABLE PRIMARY KEY `Condition`'),
    ),
    MT_APPSEARCH: (
        ('Property', 'CHAR(72) NOT NULL'),
        ('Signature_', 'CHAR(72) NOT NULL '
                       'PRIMARY KEY `Property`, `Signature_`'),
    ),
    MT_CUSTOMACTION: (
        ('Action', 'CHAR(72) NOT NULL'),
        ('Type', 'INT NOT NULL'),
        ('Source', 'CHAR(72)'),
        ('Target', 'CHAR(255)'),
        ('ExtendedType', 'LONG '
                         'PRIMARY KEY `Action`'),
    ),
    MT_REGLOCATOR: (
        ('Signature_', 'CHAR(72) NOT NULL'),
        ('Root', 'INT NOT NULL'),
        ('Key', 'CHAR(255) NOT NULL'),
        ('Name', 'CHAR(255)'),
        ('Type', 'INT '
                 'PRIMARY KEY `Signature_`'),
    ),
    MT_CREATEFOLDER: (
        ('Directory_', 'CHAR(72) NOT NULL'),
        ('Component_', 'CHAR(72) NOT NULL '
                       'PRIMARY KEY `Directory_`, `Component_`'),
    ),
    MT_SIGNATURE: (
        ('Signature', 'CHAR(72) NOT NULL'),
        ('FileName', 'CHAR(255) NOT NULL'),
        ('MinVersion', 'CHAR(20)'),
        ('MaxVersion', 'CHAR(20)'),
        ('MinSize', 'LONG'),
        ('MaxSize', 'LONG'),
        ('MinDate', 'LONG'),
        ('MaxDate', 'LONG'),
        ('Languages', 'CHAR(255) '
                      'PRIMARY KEY `Signature`'),
    ),
    MT_FILEHASH: (
        ('File_', 'CHAR(72) NOT NULL'),
        ('Options', 'INT NOT NULL'),
        ('HashPart1', 'LONG NOT NULL'),
        ('HashPart2', 'LONG NOT NULL'),
        ('HashPart3', 'LONG NOT NULL'),
        ('HashPart4', 'LONG NOT NULL '
                      'PRIMARY KEY `File_`'),
    ),
}
