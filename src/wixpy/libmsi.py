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
import os

gi.require_version('Libmsi', '1.0')
gi.require_version('GCab', '1.0')

from gi.repository import Libmsi
from gi.repository import GCab
from gi.repository import Gio

MAXINT = 4294967295


class SummaryInfo(object):
    title = None
    author = None
    subject = None
    comments = None
    template = None
    keywords = None
    codepage = None
    uuid = None
    filetime = None
    version = None
    appname = None
    security = None
    source = None

    def write_msi(self, db):
        properties = [
            (Libmsi.Property.TITLE, self.title),
            (Libmsi.Property.AUTHOR, self.author),
            (Libmsi.Property.LASTAUTHOR, self.author),
            (Libmsi.Property.SUBJECT, self.subject),
            (Libmsi.Property.COMMENTS, self.comments),
            (Libmsi.Property.TEMPLATE, self.template),
            (Libmsi.Property.KEYWORDS, self.keywords),
            (Libmsi.Property.CODEPAGE, self.codepage),
            (Libmsi.Property.UUID, self.uuid),
            (Libmsi.Property.CREATED_TM, self.filetime),
            (Libmsi.Property.LASTSAVED_TM, self.filetime),
            (Libmsi.Property.VERSION, self.version),
            (Libmsi.Property.APPNAME, self.appname),
            (Libmsi.Property.SECURITY, self.security),
            (Libmsi.Property.SOURCE, self.source), ]

        msi_prop = Libmsi.SummaryInfo.new(None, MAXINT)
        for prop, value in properties:
            if prop in [Libmsi.Property.CREATED_TM,
                        Libmsi.Property.LASTSAVED_TM]:
                msi_prop.set_filetime(prop, value)
            elif isinstance(value, int):
                msi_prop.set_int(prop, value)
            else:
                msi_prop.set_string(prop, value)
        msi_prop.save(db)


class Table(object):
    length = None
    name = None
    records = None

    def __init__(self, name, table_spec):
        self.name = name
        self.records = []
        self.length = len(table_spec)
        self.tbl_spec = table_spec

    def _create_table(self, db):
        fields = ['`%s` %s' % (name, tp)
                  for name, tp in self.tbl_spec]
        table_description = ', '.join(fields)
        sql = 'CREATE TABLE `%s` (%s)' % (self.name, table_description)
        Libmsi.Query.new(db, sql).execute()

    def _normalize_str(self, text):
        return text

    def _write_records(self, db):
        for record in self.records:
            idx = 0
            fields = []
            values = []
            for item in record:
                if item is not None:
                    fields.append('`%s`' % self.tbl_spec[idx][0])
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
                    msirec.set_string(index, self._normalize_str(item))
                elif isinstance(item, tuple) and item[0] == 'filepath':
                    msirec.load_stream(index, item[1])
                else:
                    msg = 'Incompatible type of record item: %s %s'
                    raise ValueError(msg % (str(type(item)), str(item)))
                index += 1
            query.execute(msirec)

    def write_msi(self, db):
        pass


class Database(object):
    def __init__(self):
        self.db = None
        self.files = []
        self.medias = []
        self.tables = None

    def build_cabinet(self, cabfile, compressed=True, embed=True):
        folder = GCab.Folder.new(GCab.Compression.MSZIP if compressed
                                 else GCab.Compression.NONE)
        for filepath, file_id in self.files:
            gpointer = Gio.File.new_for_path(filepath)
            folder.add_file(GCab.File.new_with_file(file_id, gpointer), False)
        cab = GCab.Cabinet.new()
        cab.add_folder(folder)
        cab.write(Gio.File.new_for_path(cabfile).replace('', False, 0, None),
                  None, None, None)
        if embed:
            self.tables['_Streams'].add(os.path.basename(cabfile),
                                        ('filepath', cabfile))

    def init_db(self, msifile):
        self.db = Libmsi.Database.new(msifile, Libmsi.DbFlags.CREATE, None)

    def commit_db(self):
        self.db.commit()

    def write_msi(self, db):
        pass
