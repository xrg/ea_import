# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Enapps LTD (<http://www.enapps.co.uk>).
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
import base64
from cStringIO import StringIO

class ea_import_template(osv.osv):
    _name='ea_import.template'
    _columns = {
        'name' : fields.char('Name', size=256),
        'target_model_id': fields.many2one('ir.model', 'Target Model'),
        'test_input_file': fields.binary('Test Importing File'),
        'header': fields.boolean('Header',),
        'line_ids': fields.one2many('ea_import.template.line', 'template_id', 'Template Lines', ),
        }

    _defaults = {
    }

    def verify_template(self, cr, uid, ids, context={}):
        for template in self.browse(cr, uid, ids, context=context):
            base_model = template.target_model_id.model
            print base64.b64decode(template.test_input_file)
        return True

    def get_header_list(self, cr, uid, ids, context={}):
        result = []
        for template in self.browse(cr, uid, ids, context=context):
            if template.header:
                input_file = StringIO(base64.b64decode(template.test_input_file))
                header_string = input_file.readline()
                input_file.close()
                result = header_string.split(',')
        return result

    def get_header_list(self, input_file):
        result_string = input_file.readline()
        return result_string.split(',')

    def get_string_by_number(self, cr, uid, ids, number, context={}):
        result = None
        for template in self.browse(cr, uid, ids, context=context):
            input_file = StringIO(base64.b64decode(template.test_input_file))
            result = input_file.readlines()[number]
        return result


ea_import_template()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
