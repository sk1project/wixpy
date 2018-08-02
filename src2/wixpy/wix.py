# -*- coding: utf-8 -*-
#
#   WiX/WiXL model
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

import os

import msi
import wixutils

WIXL = False

XMLNS = 'http://schemas.microsoft.com/wix/2006/wi'
INDENT = 4
WRAP = 3

COMPONENTS = []

ATTRS = {
    'Wix': ('xmlns',),
    'Product': ('Id', 'Name', 'UpgradeCode', 'Language', 'Codepage', 'Version',
                'Manufacturer'),
    'Package': ('Id', 'Keywords', 'Description', 'Comments', 'InstallerVersion',
                'Languages', 'Compressed', 'Manufacturer', 'SummaryCodepage',
                'Platform', 'InstallScope'),
    'Media': ('Id', 'Cabinet', 'EmbedCab', 'DiskPrompt'),
    'Property': ('Id', 'Value',),
    'Icon': ('Id', 'SourceFile',),
    'Directory': ('Id', 'Name',),
    'DirectoryRef': ('Id',),
    'Component': ('Id', 'Guid', 'Win64'),
    'ComponentRef': ('Id',),
    'File': ('Id', 'DiskId', 'Name', 'KeyPath', 'Source'),
    'Shortcut': ('Id', 'Name', 'Description', 'Target', 'WorkingDirectory'),
    'Feature': ('Id', 'Title', 'Level'),
    'RemoveFolder': ('Id', 'On'),
    'RegistryValue': ('Root', 'Key', 'Name', 'Type', 'Value', 'KeyPath'),
    'Condition': ('Message', 'Level'),
}


def defaults():
    return {
        'Description': '---',
        'Comments': '-',
        'Keywords': '---',
        # Language
        'Language': '1033',
        'Languages': '1033',
        'Codepage': '1252',
        'SummaryCodepage': '1252',
        # Internals
        'InstallerVersion': '200',
        'InstallScope': 'perMachine',
        'Compressed': 'yes',
        'KeyPath': 'yes',
        # Media
        'Cabinet': 'installer.cab',
        'EmbedCab': 'yes',
        'DiskPrompt': 'CD-ROM #1',
        'DiskId': '1',
        '_SkipHidden': True,
        '_OsCondition': '601',
    }


class WixElement(object):
    parent = None
    childs = None
    tag = None
    attrs = None
    comment = None
    is_file = False
    is_dir = False
    is_comp = False
    nl = False

    def __init__(self, parent, tag, **kwargs):
        self.parent = parent
        self.childs = []
        self.tag = tag
        self.attrs = {key: value for key, value in kwargs.items()
                      if key in ATTRS[self.tag]}
        if 'Id' not in self.attrs or self.attrs['Id'] == '*':
            self.attrs['Id'] = wixutils.get_id()
        if self.attrs.get('Guid') == '*':
            self.attrs['Guid'] = wixutils.get_guid()

    def destroy(self):
        for child in self.childs:
            child.destroy()
        for item in self.__dict__.keys():
            self.__dict__[item] = None

    def add(self, child):
        self.childs.append(child)

    def set(self, **kwargs):
        self.attrs.update(kwargs)

    def get(self, key):
        return self.attrs.get(key, '')

    def pop(self, key):
        if key in self.attrs:
            self.attrs.pop(key)

    def write_xml(self, fp, indent=0):
        if self.nl:
            fp.write('\n')
        tab = indent * ' '
        if self.comment:
            fp.write('%s<!-- %s -->\n' % (tab, self.comment))
        fp.write('%s<%s' % (tab, self.tag))
        prefix = '\n%s  ' % tab if len(self.attrs) > WRAP else ' '
        for key, value in self.attrs.items():
            fp.write('%s%s="%s"' % (prefix, key, value))
        if self.childs:
            fp.write('>\n')
            for child in self.childs:
                child.write_xml(fp, indent + INDENT)
            fp.write('%s</%s>\n' % (tab, self.tag))
        else:
            fp.write(' />\n')

    def write_msi_records(self, db):
        pass

    def write_msi(self, db):
        self.write_msi_records(db)
        if self.childs:
            for child in self.childs:
                child.write_msi(db)


class WixCondition(WixElement):
    tag = 'Condition'
    nl = True

    def __init__(self, parent, msg, condition, level=None, comment=None):
        self.comment = comment
        self.condition = condition
        super(WixCondition, self).__init__(parent, self.tag, Message=msg)
        if level:
            self.set(Level=str(level))
        self.pop('Id')

    def write_xml(self, fp, indent=0):
        if self.nl:
            fp.write('\n')
        tab = indent * ' '
        if self.comment:
            fp.write('%s<!-- %s -->\n' % (tab, self.comment))
        fp.write('%s<%s' % (tab, self.tag))
        prefix = '\n%s  ' % tab if len(self.attrs) > WRAP else ' '
        for key, value in self.attrs.items():
            fp.write('%s%s="%s"' % (prefix, key, value))
        if WIXL:
            condition = self.condition
            fp.write('>%s</%s>\n' % (condition, self.tag))
        else:
            tab_int = (indent + INDENT) * ' '
            condition = '%s<![CDATA[%s]]>' % (tab_int, self.condition)
            fp.write('>\n%s\n%s</%s>\n' % (condition, tab, self.tag))

    def write_msi_records(self, db):
        db.tables[msi.MT_LAUNCHCONDITION].add(self.condition,
                                              self.get('Message'))


OS_CONDITION = {
    '501': 'Windows XP, Windows Server 2003',
    '502': 'Windows Server 2003',
    '600': 'Windows Vista, Windows Server 2008',
    '601': 'Windows 7, Windows Server 2008R2',
    '602': 'Windows 8, Windows Server 2012',
    '603': 'Windows 8.1, Windows Server 2012 R2',
    '1000': 'Windows 10, Windows Server 2016',
}


class WixOsCondition(WixCondition):
    def __init__(self, parent, os_condition):
        comment = 'Launch Condition to check suitable system version'
        os_condition = '501' if str(os_condition) not in OS_CONDITION \
            else str(os_condition)
        msg = 'This application is only ' \
              'supported on %s or higher.' % OS_CONDITION[os_condition]
        os_condition = 'Installed OR (VersionNT >= %s)' % os_condition
        super(WixOsCondition, self).__init__(parent, msg, os_condition,
                                             comment=comment)


class WixArchCondition(WixCondition):
    def __init__(self, parent):
        comment = 'Launch Condition to check that ' \
                  'x64 installer is used on x64 systems'
        msg = '64-bit operating system was not detected, ' \
              'please use the 32-bit installer.'
        super(WixArchCondition, self).__init__(parent, msg, 'VersionNT64',
                                               comment=comment)


class WixProperty(WixElement):
    tag = 'Property'

    def __init__(self, parent, pid, value):
        super(WixProperty, self).__init__(parent, self.tag, Id=pid, Value=value)

    def write_msi_records(self, db):
        db.tables[msi.MT_PROPERTY].add(self.get('Id'), self.get('Value'))


class WixIcon(WixElement):
    tag = 'Icon'
    nl = True

    def __init__(self, parent, data):
        self.source = data.get('_Icon', '')
        super(WixIcon, self).__init__(parent, self.tag,
                                      SourceFile=data.get('_Icon', ''),
                                      Id=os.path.basename(self.source))

    def write_msi_records(self, db):
        filepath = self.get('SourceFile')
        if os.path.exists(filepath):
            db.tables[msi.MT_ICON].add(self.get('Id'), ('filepath', filepath))


class WixMedia(WixElement):
    tag = 'Media'
    nl = True

    def __init__(self, parent, data):
        super(WixMedia, self).__init__(parent, self.tag, Id='1', **data)

    def write_msi_records(self, db):
        cabinet = '#%s' % self.get('Cabinet') if self.get('EmbedCab') == 'yes' \
            else self.get('Cabinet')
        disk = int(self.get('Id'))
        rec = db.tables[msi.MT_MEDIA].add(disk, 0, self.get('DiskPrompt'),
                                          cabinet, None, None)
        db.medias.append(rec)


class WixFile(WixElement):
    tag = 'File'
    path = None
    is_file = True

    def __init__(self, parent, data, path, rel_path):
        self.path = path
        pid = wixutils.get_id('fil')
        super(WixFile, self).__init__(parent, self.tag, **data)
        self.set(Id=pid, Name=os.path.basename(rel_path), Source=path)

    def write_msi_records(self, db):
        table = db.tables[msi.MT_FILE]
        file_id = self.get('Id')
        comp_id = self.parent.get('Id')
        name = self.get('Name')
        size = os.path.getsize(self.get('Source'))
        sequence = len(table.records) + 1
        table.add(file_id, comp_id, name, size, None, None,
                  msi.FileAttribute.VITAL, sequence)
        db.files.append(self.get('Source'))


class WixComponent(WixElement):
    tag = 'Component'
    is_comp = True

    def __init__(self, parent, data, path, rel_path):
        super(WixComponent, self).__init__(parent, self.tag,
                                           Guid=wixutils.get_guid(), **data)
        self.add(WixFile(self, data, path, rel_path))
        self.set(Id=wixutils.get_id('cmp'))
        COMPONENTS.append(self.attrs['Id'])

    def write_msi_records(self, db):
        attr = msi.ComponentAttribute.LOCAL_ONLY
        key = None
        if self.get('Win64') == 'yes':
            attr |= msi.ComponentAttribute.X64
        if any([child.tag == 'RegistryValue' for child in self.childs]):
            attr |= msi.ComponentAttribute.REGISTRY_KEY_PATH
            for child in self.childs:
                if child.tag == 'RegistryValue':
                    key = child.get('Key')
                    break
        elif self.childs[0].tag == 'File':
            key = self.childs[0].get('Id')

        table = db.tables[msi.MT_MEDIA]
        table.add(self.get('Id'), '{%s}' % self.get('Guid'),
                  self.parent.get('Id'), attr, None, key)


class WixDirectory(WixElement):
    tag = 'Directory'
    is_dir = True

    def __init__(self, parent, data=None, path=None, rel_path=None, **kwargs):
        name = kwargs['Name'] if 'Name' in kwargs \
            else os.path.basename(rel_path)
        pid = kwargs['Id'] if 'Id' in kwargs \
            else wixutils.get_id('dir')
        super(WixDirectory, self).__init__(parent, self.tag, Id=pid, Name=name)

        if data is not None:
            for item in os.listdir(path):
                if data.get('_SkipHidden') and item.startswith('.'):
                    continue
                item_path = os.path.join(path, item)
                item_rel_path = os.path.join(rel_path, item)
                if os.path.isdir(item_path):
                    self.add(WixDirectory(self, data, item_path, item_rel_path))
                elif os.path.isfile(item_path):
                    self.add(WixComponent(self, data, item_path, item_rel_path))

    def write_msi_records(self, db):
        table = db.tables[msi.MT_DIRECTORY]
        table.add(self.get('Id'), self.parent.get('Id'),
                  self.get('Name') or '.')


class WixInstallDir(WixElement):
    tag = 'Directory'
    is_dir = True

    def __init__(self, parent, data):
        super(WixInstallDir, self).__init__(parent, self.tag,
                                            Id='INSTALLDIR',
                                            Name=data.get('_InstallDir'))
        path = data.get('_SourceDir')
        rel_path = os.path.basename(path)
        # Recursive scan start
        for item in os.listdir(path):
            if data.get('_SkipHidden') and item.startswith('.'):
                continue
            item_path = os.path.join(path, item)
            item_rel_path = os.path.join(rel_path, item)
            if os.path.isdir(item_path):
                self.add(WixDirectory(self, data, item_path, item_rel_path))
            elif os.path.isfile(item_path):
                self.add(WixComponent(self, data, item_path, item_rel_path))

    def write_msi_records(self, db):
        table = db.tables[msi.MT_DIRECTORY]
        table.add(self.get('Id'), self.parent.get('Id'), self.get('Name'))


class WixPfDir(WixElement):
    tag = 'Directory'
    is_dir = True

    def __init__(self, parent, data):
        pid = 'ProgramFiles64Folder' if data.get('Win64') == 'yes' \
            else 'ProgramFilesFolder'
        super(WixPfDir, self).__init__(parent, self.tag, Id=pid, Name='PFiles')
        self.add(WixInstallDir(self, data))

    def write_msi_records(self, db):
        table = db.tables[msi.MT_DIRECTORY]
        table.add(self.get('Id'), self.parent.get('Id'), self.get('Name'))


class WixTargetDir(WixElement):
    tag = 'Directory'
    is_dir = True
    nl = True

    def __init__(self, parent, data):
        self.comment = 'Installed file tree'
        super(WixTargetDir, self).__init__(parent, self.tag,
                                           Id='TARGETDIR', Name='SourceDir')
        self.add(WixPfDir(self, data))

    def write_msi_records(self, db):
        table = db.tables[msi.MT_DIRECTORY]
        table.add(self.get('Id'), None, self.get('Name'))


class WixFeature(WixElement):
    tag = 'Feature'
    nl = True

    def __init__(self, parent, data):
        super(WixFeature, self).__init__(parent, self.tag,
                                         Title=data.get('Name'), Level='1')
        for item in COMPONENTS:
            self.add(WixComponentRef(self, Id=item))

    def write_msi_records(self, db):
        table = db.tables[msi.MT_FEATURE]
        parent = self.parent.get('Id') if self.parent.tag == 'Feature' else None
        table.add(self.get('Id'), parent, self.get('Title'),
                  self.get('Description'), msi.FeatureDisplay.COLLAPSE,
                  int(self.get('Level')), self.get('ConfigurableDirectory'), 0)


class WixShortcut(WixElement):
    tag = 'Shortcut'

    def __init__(self, parent, shortcut_data):
        super(WixShortcut, self).__init__(parent, self.tag, **shortcut_data)


class WixRemoveFolder(WixElement):
    tag = 'RemoveFolder'

    def __init__(self, parent, **kwargs):
        super(WixRemoveFolder, self).__init__(parent, self.tag, **kwargs)

    def write_msi_records(self, db):
        table = db.tables[msi.MT_REMOVEFILE]
        condition = msi.InstallMode.from_string(self.get('On'))
        table.add(self.get('Id'), self.parent('Id'), None,
                  self.parent.parent.get('Id'), condition)


class WixRegistryValue(WixElement):
    tag = 'RegistryValue'

    def __init__(self, parent, **kwargs):
        super(WixRegistryValue, self).__init__(parent, self.tag, **kwargs)
        pid = wixutils.get_id('reg')
        self.set(Id=pid)

    def write_msi_records(self, db):
        table = db.tables[msi.MT_REGISTRY]
        reg_id = self.get('Id')
        reg_root = msi.RegistryRoot.from_string(self.get('Root'))
        reg_key = self.get('Key')
        reg_name = self.get('Name')
        reg_comp = self.parent.get('Id')
        reg_value = self.get('Value')
        if not reg_value.startswith('#'):
            reg_value = '#' + reg_value
        table.add(reg_id, reg_root, reg_key, reg_name, reg_value, reg_comp)


class WixDirectoryRef(WixElement):
    tag = 'DirectoryRef'

    def __init__(self, parent, **kwargs):
        super(WixDirectoryRef, self).__init__(parent, self.tag, **kwargs)


class WixComponentRef(WixElement):
    tag = 'ComponentRef'

    def __init__(self, parent, **kwargs):
        super(WixComponentRef, self).__init__(parent, self.tag, **kwargs)

    def write_msi_records(self, db):
        table = db.tables[msi.MT_FEATURECOMPONENTS]
        table.add(self.parent.get('Id'), self.get('Id'))


class WixShortcutComponent(WixElement):
    tag = 'Component'

    def __init__(self, parent, data, shortcut_data):
        pid = wixutils.get_id()
        guid = wixutils.get_guid()
        super(WixShortcutComponent, self).__init__(parent, self.tag,
                                                   Guid=guid, **data)
        self.add(WixShortcut(self, shortcut_data))
        self.add(WixRemoveFolder(self, Id=shortcut_data['DirectoryRef'],
                                 On='uninstall'))
        reg_key = 'Software\\%s\\%s' % (data['Manufacturer'].replace(' ', '_'),
                                        data['Name'].replace(' ', '_'))
        self.add(WixRegistryValue(self, Root='HKCU', Key=reg_key,
                                  Name=shortcut_data['Name'], Type='integer',
                                  Value='1', KeyPath='yes'))
        self.set(Id='cmp%s' % pid)
        COMPONENTS.append(self.attrs['Id'])


class WixPackage(WixElement):
    tag = 'Package'

    def __init__(self, parent, data):
        super(WixPackage, self).__init__(parent, self.tag, **data)
        if not WIXL:
            self.set(Platform='x64' if data.get('Win64') else 'x86')

    def write_msi_records(self, db):
        if self.get('InstallScope') == "perMachine":
            db.tables[msi.MT_PROPERTY].add('ALLUSERS', '1')


class WixProduct(WixElement):
    tag = 'Product'

    def __init__(self, parent, data):
        super(WixProduct, self).__init__(parent, self.tag, **data)
        self.set(Id=wixutils.get_guid())
        self.add(WixPackage(self, data))
        COMPONENTS[:] = []
        self.add(WixMedia(self, data))
        media_name = '%s %s Installation' % (data['Name'], data['Version'])
        self.add(WixProperty(self, 'DiskPrompt', media_name))

        if data.get('_OsCondition'):
            self.add(WixOsCondition(self, data['_OsCondition']))
        if data.get('_CheckX64'):
            self.add(WixArchCondition(self))
        if data.get('_Conditions'):
            for msg, cnd in data['_Conditions']:
                self.add(WixCondition(self, msg, cnd))

        if data.get('_Icon'):
            self.add(WixIcon(self, data))
            icon_name = os.path.basename(data['_Icon'])
            self.add(WixProperty(self, 'ARPPRODUCTICON', icon_name))
        target_dir = WixTargetDir(self, data)
        self.add(target_dir)

        if data.get('_Shortcuts') and data.get('_ProgramMenuFolder'):
            pm_dir = WixDirectory(self, Id='ProgramMenuFolder', Name='')
            pm_dir.pop('Name')
            pm_dir.comment = 'Application ProgramMenu folder'
            target_dir.add(pm_dir)
            shortcut_dir = WixDirectory(self, Id=wixutils.get_id('mnu'),
                                        Name=data.get('_ProgramMenuFolder'))
            pm_dir.add(shortcut_dir)
            ref = shortcut_dir.attrs['Id']

            dir_ref = WixDirectoryRef(self, Id=ref)
            self.add(dir_ref)
            for shortcut in data.get('_Shortcuts'):
                target = os.path.join(data['_SourceDir'], shortcut['Target'])
                work_dir_id, target_id = self.find_by_path(target_dir, target)
                shortcut_data = {
                    'DirectoryRef': ref,
                    'WorkingDirectory': work_dir_id,
                }
                shortcut_data.update(shortcut)
                shortcut_data['Target'] = '[#%s]' % target_id
                dir_ref.add(WixShortcutComponent(dir_ref, data, shortcut_data))

        if COMPONENTS:
            self.add(WixFeature(self, data))

    def find_by_path(self, parent, path):
        work_dir_id = target_id = None
        for item in parent.childs:
            if item.is_comp and item.childs[0].path == path:
                work_dir_id = parent.attrs['Id']
                target_id = item.childs[0].attrs['Id']
                return work_dir_id, target_id
            elif item.is_dir:
                work_dir_id, target_id = self.find_by_path(item, path)
                if work_dir_id is not None:
                    return work_dir_id, target_id
        return work_dir_id, target_id

    def write_msi_records(self, db):
        table = db.tables[msi.MT_PROPERTY]
        table.add('Manufacturer', self.get('Manufacturer'))
        table.add('ProductLanguage', self.get('Language'))
        table.add('ProductCode', '{%s}' % self.get('Id'))
        table.add('ProductName', self.get('Name'))
        table.add('ProductVersion', self.get('Version'))
        table.add('UpgradeCode', '{%s}' % self.get('UpgradeCode'))


class Wix(WixElement):
    tag = 'Wix'

    def __init__(self, data):
        self.msi_data = defaults()
        self.msi_data.update(data)
        wixutils.MSI_ENCODING = 'cp%s' % self.msi_data['Codepage']
        self.source_dir = self.msi_data.get('_SourceDir', '.')
        super(Wix, self).__init__(None, self.tag, xmlns=XMLNS)
        self.pop('Id')
        self.add(WixProduct(self, self.msi_data))
        self.comment = 'Generated by %s %s' % \
                       (data['_pkgname'], data['_pkgver'])

    def write_xml(self, fp, indent=0):
        tab = indent * ' '
        enc = wixutils.DEFAULT_ENCODING
        fp.write('%s<?xml version="1.0" encoding="%s"?>\n' % (tab, enc))
        super(Wix, self).write_xml(fp, indent)

    def get_product(self):
        return self.childs[0]

    def get_package(self):
        return self.get_product().childs[0]

    def get_media(self):
        return self.get_product().childs[1]
