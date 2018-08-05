# -*- coding: utf-8 -*-
#
#   libmsi gobject wrapper
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

import gi

from wixpy import msi
from wixpy import utils

gi.require_version('Libmsi', '1.0')

from gi.repository import Libmsi

MAXINT = 4294967295


def msi_str(text):
    return text.decode('utf-8').encode('cp%s' % msi.MSI_CODEPAGE) \
        if not utils.IS_PY3 else text


class MsiSummaryInfo(object):
    properties = None

    def __init__(self, model):
        self.properties = []

        # Wix model root nodes
        prod = model.get_product()
        pkg = model.get_package()

        # MSI info data
        title = msi_str('%s Installation Database' % prod.get('Name'))
        author = msi_str(prod.get('Manufacturer'))
        subject = msi_str(pkg.get('Description'))
        comments = msi_str(pkg.get('Comments'))
        arch = 'x64' if pkg.get('Platform') == 'x64' else 'Intel'
        template = '%s;%s' % (arch, pkg.get('Languages'))
        keywords = msi_str(pkg.get('Keywords'))
        codepage = int(pkg.get('SummaryCodepage'))
        uuid = prod.get('Id')
        filetime = utils.filetime_now()
        version = int(pkg.get('InstallerVersion'))
        version = 200 if arch == 'x64' and version < 200 else version
        appname = msi_str(prod.get('Name'))
        security = 2

        source = msi.SourceFlags.COMPRESSED
        if pkg.get('InstallScope') == "perUser":
            source |= msi.SourceFlags.NO_PRIVILEGES

        self.add(Libmsi.Property.TITLE, title)
        self.add(Libmsi.Property.AUTHOR, author)
        self.add(Libmsi.Property.LASTAUTHOR, author)
        self.add(Libmsi.Property.SUBJECT, subject)
        self.add(Libmsi.Property.COMMENTS, comments)
        self.add(Libmsi.Property.TEMPLATE, template)
        self.add(Libmsi.Property.KEYWORDS, keywords)
        self.add(Libmsi.Property.CODEPAGE, codepage)
        self.add(Libmsi.Property.UUID, uuid)
        self.add(Libmsi.Property.CREATED_TM, filetime)
        self.add(Libmsi.Property.LASTSAVED_TM, filetime)
        self.add(Libmsi.Property.VERSION, version)
        self.add(Libmsi.Property.APPNAME, appname)
        self.add(Libmsi.Property.SECURITY, security)
        self.add(Libmsi.Property.SOURCE, source)

    def add(self, prop, value):
        self.properties.append((prop, value))

    def write_msi(self, db):
        msi_prop = Libmsi.SummaryInfo.new(None, MAXINT)
        for prop, value in self.properties:
            if prop in [Libmsi.Property.CREATED_TM,
                        Libmsi.Property.LASTSAVED_TM]:
                msi_prop.set_filetime(prop, value)
            elif isinstance(value, int):
                msi_prop.set_int(prop, value)
            else:
                msi_prop.set_string(prop, value)
        msi_prop.save(db)


class MsiTable(object):
    length = None
    name = None
    records = None

    def __init__(self, name):
        self.name = name
        self.records = []
        self.length = len(msi.MT_TABLES[self.name])

    def add(self, *args):
        if len(args) != self.length:
            raise ValueError('Incorrect number of members for record!')
        self.records.append(args)
        return args

    def add_action(self, action):
        self.add(action, msi.MSI_ACTIONS[action][0], msi.MSI_ACTIONS[action][1])

    def write_msi(self, db):
        # Create table
        if not self.name.startswith('_'):
            fields = ['`%s` %s' % (name, tp)
                      for name, tp in msi.MT_TABLES[self.name]]
            table_description = ', '.join(fields)
            sql = 'CREATE TABLE `%s` (%s)' % (self.name, table_description)
            Libmsi.Query.new(db, sql).execute()

        for record in self.records:
            idx = 0
            fields = []
            values = []
            for item in record:
                if item is not None:
                    fields.append('`%s`' % msi.MT_TABLES[self.name][idx][0])
                    values.append('?')
                idx += 1

            sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % \
                  (self.name, ', '.join(fields), ', '.join(values))
            query = Libmsi.Query.new(db, sql)

            msirec = Libmsi.Record.new(len(fields))
            index = 1
            for item in record:
                if isinstance(item, int):
                    msirec.set_int(index, item)
                elif item is None:
                    index -= 1
                elif isinstance(item, str):
                    msirec.set_string(index, msi_str(item))
                elif isinstance(item, tuple) and item[0] == 'filepath':
                    msirec.load_stream(index, item[1])
                elif self.name == '_Streams' and index == 2:
                    # TODO: implement item streaming
                    msirec.set_stream(index, item)
                else:
                    raise ValueError('Incompatible type of record item: %s %s' %
                                     (str(type(item)), str(item)))
                index += 1
            query.execute(msirec)


class MsiDatabase(object):
    model = None

    def __init__(self, model):
        self.model = model
        self.medias = []
        self.files = []
        self.tables = {key: MsiTable(key) for key in msi.MT_TABLES.keys()}

    def set_sequences(self):
        # AdminExecuteSequence
        tb = self.tables[msi.MT_ADMINEXECUTESEQUENCE]
        tb.add_action('CostInitialize')
        tb.add_action('FileCost')
        tb.add_action('CostFinalize')
        tb.add_action('InstallValidate')
        tb.add_action('InstallInitialize')
        tb.add_action('InstallAdminPackage')
        tb.add_action('InstallFiles')
        tb.add_action('InstallFinalize')

        # AdminUISequence
        tb = self.tables[msi.MT_ADMINUISEQUENCE]
        tb.add_action('CostInitialize')
        tb.add_action('FileCost')
        tb.add_action('CostFinalize')
        tb.add_action('ExecuteAction')

        # AdvtExecuteSequence
        tb = self.tables[msi.MT_ADVTEXECUTESEQUENCE]
        tb.add_action('CostInitialize')
        tb.add_action('CostFinalize')
        tb.add_action('InstallValidate')
        tb.add_action('InstallInitialize')
        tb.add_action('PublishFeatures')
        tb.add_action('PublishProduct')
        tb.add_action('InstallFinalize')
        if self.tables[msi.MT_SHORTCUT].records:
            tb.add_action('CreateShortcuts')

        # InstallExecuteSequence
        tb = self.tables[msi.MT_INSTALLEXECUTESEQUENCE]
        tb.add_action('ValidateProductID')
        tb.add_action('CostInitialize')
        tb.add_action('FileCost')
        tb.add_action('CostFinalize')
        tb.add_action('InstallValidate')
        tb.add_action('InstallInitialize')
        tb.add_action('ProcessComponents')
        tb.add_action('UnpublishFeatures')
        tb.add_action('RegisterUser')
        tb.add_action('RegisterProduct')
        tb.add_action('PublishFeatures')
        tb.add_action('PublishProduct')
        tb.add_action('InstallFinalize')
        if self.tables[msi.MT_UPGRADE].records:
            tb.add_action('FindRelatedProducts')
            tb.add_action('MigrateFeatureStates')
        if self.tables[msi.MT_LAUNCHCONDITION].records:
            tb.add_action('LaunchConditions')
        if self.tables[msi.MT_REGISTRY].records:
            tb.add_action('RemoveRegistryValues')
            tb.add_action('WriteRegistryValues')
        if self.tables[msi.MT_SHORTCUT].records:
            tb.add_action('RemoveShortcuts')
            tb.add_action('CreateShortcuts')
        if self.tables[msi.MT_FILE].records:
            tb.add_action('RemoveFiles')
            tb.add_action('InstallFiles')
        if not self.tables[msi.MT_FILE].records and \
                self.tables[msi.MT_REMOVEFILE].records:
            tb.add_action('RemoveFiles')
        if self.tables[msi.MT_SERVICECONTROL].records:
            tb.add_action('StartServices')
            tb.add_action('StopServices')
            tb.add_action('DeleteServices')
        if self.tables[msi.MT_SERVICEINSTALL].records:
            tb.add_action('InstallServices')
        if self.tables[msi.MT_CREATEFOLDER].records:
            tb.add_action('RemoveFolders')
            tb.add_action('CreateFolders')
        if self.tables[msi.MT_APPSEARCH].records:
            tb.add_action('AppSearch')

        # InstallUISequence
        tb = self.tables[msi.MT_INSTALLUISEQUENCE]
        tb.add_action('ValidateProductID')
        tb.add_action('CostInitialize')
        tb.add_action('FileCost')
        tb.add_action('CostFinalize')
        tb.add_action('ExecuteAction')
        if self.tables[msi.MT_UPGRADE].records:
            tb.add_action('FindRelatedProducts')
            tb.add_action('MigrateFeatureStates')
        if self.tables[msi.MT_LAUNCHCONDITION].records:
            tb.add_action('LaunchConditions')
        if self.tables[msi.MT_APPSEARCH].records:
            tb.add_action('AppSearch')

    def write_msi(self, filename):
        db = Libmsi.Database.new(filename, Libmsi.DbFlags.CREATE, None)
        utils.echo_msg('Writing SummaryInfo')
        MsiSummaryInfo(self.model).write_msi(db)
        utils.echo_msg('Building tables...')
        self.model.write_msi(self)
        utils.echo_msg('Creating sequences...')
        self.set_sequences()
        utils.echo_msg('Writing tables...')
        for item in self.tables.items():
            utils.echo_msg('\tWriting %s table...' % item[0])
            item[1].write_msi(db)
        utils.echo_msg('All tables processed')
        db.commit()
