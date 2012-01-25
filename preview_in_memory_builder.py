# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from osv import fields
import datetime
import math
from dateutil import parser
import report
from tools.translate import _
import time
import netsvc
import crm
import copy

#class preview_in_memory_builder(osv.osv_memory):

    #def __init__(self, pool, cr, module_name):
        #osv.osv_memory.__init__(self, pool, cr)
        #self.doinit = True
        #self.unlink_mark = {}

        #if getattr(pool, 'model_data_reference_ids', None) is None:
            #self.pool.model_data_reference_ids = {}
        #self.loads = self.pool.model_data_reference_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
