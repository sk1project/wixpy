# -*- coding: utf-8 -*-
#
#   libmsi gobject wrapper
#
# 	Copyright (C) 2018 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi

import wixutils

gi.require_version('Libmsi', '1.0')

from gi.repository import Libmsi

msi_str = wixutils.msi_str
MAXINT = 4294967295


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
        template = msi_str('%s;%s' % (arch, pkg.get('Languages')))
        keywords = msi_str(pkg.get('Keywords'))
        codepage = int(pkg.get('SummaryCodepage'))
        uuid = msi_str(prod.get('Id'))
        filetime = wixutils.filetime_now()
        version = int(pkg.get('InstallerVersion'))
        version = 200 if arch == 'x64' and version < 200 else version
        appname = msi_str(prod.get('Name'))
        security = 2

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


class MsiDatabase(object):
    model = None

    def __init__(self, model):
        self.model = model
        self.tables = {}

    def write_msi(self, filename):
        db = Libmsi.Database.new(filename, Libmsi.DbFlags.CREATE, None)
        MsiSummaryInfo(self.model).write_msi(db)
        for item in self.tables.items():
            item[1].write_msi(db)
        db.commit()
