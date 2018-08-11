# -*- coding: utf-8 -*-
#
#   _msi extension wrapper
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
import _msi


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
        si = db.GetSummaryInformation(20)
        si.SetProperty(_msi.PID_TITLE, self.title)
        si.SetProperty(_msi.PID_SUBJECT, self.subject)
        si.SetProperty(_msi.PID_AUTHOR, self.author)
        si.SetProperty(_msi.PID_TEMPLATE, self.template)
        si.SetProperty(_msi.PID_REVNUMBER, self.uuid)
        si.SetProperty(_msi.PID_WORDCOUNT, self.source)
        si.SetProperty(_msi.PID_PAGECOUNT, self.version)
        si.SetProperty(_msi.PID_APPNAME, self.appname)
        si.SetProperty(_msi.PID_COMMENTS, self.comments)
        si.SetProperty(_msi.PID_KEYWORDS, self.keywords)
        si.SetProperty(_msi.PID_CODEPAGE, self.codepage)
        si.SetProperty(_msi.PID_SECURITY, self.security)


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
        fields = ['`%s` %s' % (name, tp) for name, tp in self.tbl_spec]
        table_description = ', '.join(fields)
        sql = 'CREATE TABLE `%s` (%s)' % (self.name, table_description)
        db_view = db.OpenView(sql)
        db_view.Execute(None)
        db_view.Close()

    def _normalize_str(self, text):
        return text

    def _write_records(self, db):
        db_view = db.OpenView('SELECT * FROM `%s`' % self.name)
        count = db_view.GetColumnInfo(_msi.MSICOLINFO_NAMES).GetFieldCount()
        msirec = _msi.CreateRecord(count)
        for record in self.records:
            for i in range(count):
                field = record[i]
                if isinstance(field, (int, long)):
                    msirec.SetInteger(i + 1, field)
                elif isinstance(field, basestring):
                    msirec.SetString(i + 1, field)
                elif field is None:
                    pass
                elif isinstance(field, tuple) and field[0] == 'filepath':
                    msirec.SetStream(i + 1, field[1])
                else:
                    msg = 'Incompatible type of record item: %s %s'
                    raise ValueError(msg % (str(type(field)), str(field)))
            try:
                db_view.Modify(_msi.MSIMODIFY_INSERT, msirec)
            except Exception as e:
                raise Exception('Could not insert %s into %s: %s' %
                                (repr(record), self.name, repr(e)))
            msirec.ClearData()
        db_view.Close()

    def write_msi(self, db):
        pass


class Database(object):
    def __init__(self):
        self.db = None
        self.files = []
        self.medias = []
        self.tables = None

    def build_cabinet(self, cabfile, compressed=True, embed=True):
        _msi.FCICreate(cabfile, self.files)
        if embed:
            self.tables['_Streams'].add(os.path.basename(cabfile),
                                        ('filepath', cabfile))

    def init_db(self, msifile):
        self.db = _msi.OpenDatabase(msifile, _msi.MSIDBOPEN_CREATE)

    def commit_db(self):
        self.db.Commit()

    def write_msi(self, db):
        pass
