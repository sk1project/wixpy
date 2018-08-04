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

MSI_ENCODING
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

    def write_msi(self, db):
        # Create table
        if not self.name.startswith('_'):
            fields = ['`%s` %s' % (name, tp)
                      for name, tp in msi.MT_TABLES[self.name]]
            table_description = ', '.join(fields)
            sql = 'CREATE TABLE `%s` (%s)' % (self.name, table_description)
            Libmsi.Query.new(db, sql).execute()

        # Write records
        if not self.records:
            return

        idx = 0
        fields = []
        values = []
        for item in self.records[0]:
            if item is not None:
                fields.append('`%s`' % msi.MT_TABLES[self.name][idx][0])
                values.append('?')
            idx += 1

        sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % \
              (self.name, ', '.join(fields), ', '.join(values))
        query = Libmsi.Query.new(db, sql)
        for record in self.records:
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
        self.tables = {}
        self.medias = []
        self.files = []
        for key in msi.MT_TABLES.keys():
            self.tables[key] = MsiTable(key)

    def write_msi(self, filename):
        db = Libmsi.Database.new(filename, Libmsi.DbFlags.CREATE, None)
        utils.echo_msg('Writing SummaryInfo')
        MsiSummaryInfo(self.model).write_msi(db)
        utils.echo_msg('Building tables...')
        self.model.write_msi(self)
        # for item in self.tables.items():
        #     utils.echo_msg('\tWriting %s table...' % item[0])
        #     item[1].write_msi(db)
        # utils.echo_msg('All tables processed')
        db.commit()
