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

MSI_CODEPAGE = '1252'


# ----------- MSI enums -----------


class SourceFlags(object):
    SHORT_NAMES = 1 << 0
    COMPRESSED = 1 << 1
    ADMIN = 1 << 2
    NO_PRIVILEGES = 1 << 3


class ComponentAttribute(object):
    LOCAL_ONLY = 0
    SOURCE_ONLY = 1 << 0
    OPTIONAL = 1 << 1
    REGISTRY_KEY_PATH = 1 << 2
    SHARED_DLL_REF_COUNT = 1 << 3
    PERMANENT = 1 << 4
    ODBC_DATA_SOURCE = 1 << 5
    TRANSITIVE = 1 << 6
    NEVER_OVERWRITE = 1 << 7
    X64 = 1 << 8
    REGISTRY_REFLECTION = 1 << 9
    UNINSTALL_ON_SUPERSEDENCE = 1 << 10
    SHARED = 1 << 11


class FeatureDisplay(object):
    HIDDEN = 0
    EXPAND = 1 << 0
    COLLAPSE = 1 << 1


class InstallMode(object):
    INSTALL = 1 << 0
    UNINSTALL = 1 << 1
    BOTH = 1 << 2

    @classmethod
    def from_string(cls, str_value):
        return {'install': cls.INSTALL,
                'uninstall': cls.UNINSTALL,
                'both': cls.BOTH}[str_value.lower()]


class RegistryValueType(object):
    STRING = 1 << 0
    INTEGER = 1 << 1
    BINARY = 1 << 2
    EXPANDABLE = 1 << 3
    MULTI_STRING = 1 << 4

    @classmethod
    def from_string(cls, str_value):
        return {'string': cls.STRING,
                'integer': cls.INTEGER,
                'binary': cls.BINARY,
                'expandable': cls.EXPANDABLE,
                'multistring': cls.MULTI_STRING}[str_value.lower()]


class RegistryRoot(object):
    HKCR = 1 << 0
    HKCU = 1 << 1
    HKLM = 1 << 2
    HKU = 1 << 3
    HKMU = 1 << 4

    @classmethod
    def from_string(cls, str_value):
        return {'HKCR': cls.HKCR,
                'HKCU': cls.HKCU,
                'HKLM': cls.HKLM,
                'HKU': cls.HKU,
                'HKMU': cls.HKMU}[str_value.upper()]


class FileAttribute(object):
    READ_ONLY = 1 << 0
    HIDDEN = 1 << 1
    SYSTEM = 1 << 2
    VITAL = 1 << 9
    CHECKSUM = 1 << 10
    PATCH_ADDED = 1 << 11
    NON_COMPRESSED = 1 << 12
    COMPRESSED = 1 << 13


class UpgradeAttribute(object):
    MIGRATE_FEATURES = 1 << 0
    ONLY_DETECT = 1 << 1
    IGNORE_REMOVE_FAILURE = 1 << 2
    VERSION_MIN_INCLUSIVE = 1 << 8
    VERSION_MAX_INCLUSIVE = 1 << 9
    LANGUAGES_EXCLUSIVE = 1 << 10


class ServiceControlEvent(object):
    INSTALL_START = 1 << 0
    INSTALL_STOP = 1 << 1
    INSTALL_DELETE = 1 << 3
    UNINSTALL_START = 1 << 4
    UNINSTALL_STOP = 1 << 5
    UNINSTALL_DELETE = 1 << 7


class ActionFlags(object):
    ADMIN_EXECUTE_SEQUENCE = 1 << 0
    ADMIN_UI_SEQUENCE = 1 << 1
    ADVT_EXECUTE_SEQUENCE = 1 << 2
    INSTALL_EXECUTE_SEQUENCE = 1 << 3
    INSTALL_UI_SEQUENCE = 1 << 4
    ALL = -1


MSI_ACTIONS = {
    'InstallInitialize': (None, 1500, ActionFlags.ADMIN_EXECUTE_SEQUENCE |
                          ActionFlags.ADVT_EXECUTE_SEQUENCE |
                          ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'InstallExecute': ('NOT Installed', 6500,
                       ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'InstallExecuteAgain': ('NOT Installed', 6550,
                            ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'InstallFinalize': (None, 6600, ActionFlags.ADMIN_EXECUTE_SEQUENCE |
                        ActionFlags.ADVT_EXECUTE_SEQUENCE |
                        ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'InstallFiles': (None, 4000, ActionFlags.ADMIN_EXECUTE_SEQUENCE |
                     ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'InstallAdminPackage': (None, 3900, ActionFlags.ADMIN_EXECUTE_SEQUENCE),
    'FileCost': (None, 900, ActionFlags.ADMIN_EXECUTE_SEQUENCE |
                 ActionFlags.ADMIN_UI_SEQUENCE |
                 ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                 ActionFlags.INSTALL_UI_SEQUENCE),
    'CostInitialize': (None, 800, ActionFlags.ALL),
    'CostFinalize': (None, 1000, ActionFlags.ALL),
    'InstallValidate': (None, 1400, ActionFlags.ADMIN_EXECUTE_SEQUENCE |
                        ActionFlags.ADVT_EXECUTE_SEQUENCE |
                        ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'ExecuteAction': (None, 1300, ActionFlags.ADMIN_UI_SEQUENCE |
                      ActionFlags.INSTALL_UI_SEQUENCE),
    'CreateShortcuts': (None, 4500, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                        ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'MsiPublishAssemblies': (None, 6250, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                             ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'PublishComponents': (None, 6200, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                          ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'PublishFeatures': (None, 6300, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                        ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'PublishProduct': (None, 6400, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                       ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterClassInfo': (None, 4600, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                          ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterExtensionInfo': (None, 4700, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                              ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterMIMEInfo': (None, 4900, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                         ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterProgIdInfo': (None, 4800, ActionFlags.ADVT_EXECUTE_SEQUENCE |
                           ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'AllocateRegistrySpace': ('NOT Installed', 1550,
                              ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'AppSearch': (None, 50, ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                  ActionFlags.INSTALL_UI_SEQUENCE),
    'BindImage': (None, 4300, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'CCPSearch': ('NOT Installed', 500, ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                  ActionFlags.INSTALL_UI_SEQUENCE),
    'CreateFolders': (None, 3700, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'DeleteServices': ('VersionNT', 2000, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'DuplicateFiles': (None, 4210, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'FindRelatedProducts': (None, 25, ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                            ActionFlags.INSTALL_UI_SEQUENCE),
    'InstallODBC': (None, 5400, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'InstallServices': ('VersionNT', 5800,
                        ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'MsiConfigureServices': ('VersionNT>=600', 5850,
                             ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'IsolateComponents': (None, 950, ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                          ActionFlags.INSTALL_UI_SEQUENCE),
    'LaunchConditions': (None, 100, ActionFlags.ADMIN_EXECUTE_SEQUENCE |
                         ActionFlags.ADMIN_UI_SEQUENCE |
                         ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                         ActionFlags.INSTALL_UI_SEQUENCE),
    'MigrateFeatureStates': (None, 1200, ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                             ActionFlags.INSTALL_UI_SEQUENCE),
    'MoveFiles': (None, 3800, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'PatchFiles': (None, 4090, ActionFlags.ADMIN_EXECUTE_SEQUENCE |
                   ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'ProcessComponents': (None, 1600, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterComPlus': (None, 5700, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterFonts': (None, 5300, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterProduct': (None, 6100, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterTypeLibraries': (None, 5500, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RegisterUser': (None, 6000, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RemoveDuplicateFiles': (None, 3400, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RemoveEnvironmentStrings': (None, 3300,
                                 ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RemoveFiles': (None, 3500, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RemoveFolders': (None, 3600, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RemoveIniValues': (None, 3100, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RemoveODBC': (None, 2400, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RemoveRegistryValues': (None, 2600, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RemoveShortcuts': (None, 3200, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'RMCCPSearch': ('NOT Installed', 600, ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                    ActionFlags.INSTALL_UI_SEQUENCE),
    'SelfRegModules': (None, 5600, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'SelfUnregModules': (None, 2200, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'SetODBCFolders': (None, 1100, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'StartServices': ('VersionNT', 5900, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'StopServices': ('VersionNT', 1900, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'MsiUnpublishAssemblies': (None, 1750,
                               ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnpublishComponents': (None, 1700, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnpublishFeatures': (None, 1800, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnregisterClassInfo': (None, 2700, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnregisterComPlus': (None, 2100, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnregisterExtensionInfo': (None, 2800,
                                ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnregisterFonts': (None, 2500, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnregisterMIMEInfo': (None, 3000, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnregisterProgIdInfo': (None, 2900, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'UnregisterTypeLibraries': (None, 2300,
                                ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'ValidateProductID': (None, 700, ActionFlags.INSTALL_EXECUTE_SEQUENCE |
                          ActionFlags.INSTALL_UI_SEQUENCE),
    'WriteEnvironmentStrings': (None, 5200,
                                ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'WriteIniValues': (None, 5100, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
    'WriteRegistryValues': (None, 5000, ActionFlags.INSTALL_EXECUTE_SEQUENCE),
}

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
MT_ERROR = 'Error'
MT_ENVIRONMENT = 'Environment'

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
    MT_ERROR: (
        ('Error', 'INT NOT NULL'),
        ('Message', 'CHAR(0) LOCALIZABLE '
                    'PRIMARY KEY `Error`'),
    ),
    MT_ENVIRONMENT: (
        ('Environment', 'CHAR(72) NOT NULL'),
        ('Name', 'CHAR(255) NOT NULL'),
        ('Value', 'CHAR(255)'),
        ('Component_', 'CHAR(72) NOT NULL '
                       'PRIMARY KEY `Environment`'),
    ),
}
