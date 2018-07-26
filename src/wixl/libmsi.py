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

gi.require_version('Libmsi', '1.0')

from gi.repository import Libmsi


class MsiSummaryInfo(object):
    properties = None

    def __init__(self, model):
        self.properties = []
        prod = model.get_product()
        pack = model.get_package()
        media = model.get_media()
        msiprop = Libmsi.Property
        self.add(msiprop.TITLE, "%s Installation Database" % prod.get('Name'))

    def add(self, prop, value):
        self.properties.append((prop, value))


class MsiDatabase(object):
    model = None

    def __init__(self, model):
        self.model = model

    def write_msi(self, filename):
        db = Libmsi.Database.new(filename, Libmsi.DbFlags.CREATE, None)
        # TODO: write info
        # TODO: write tables
        db.commit()
