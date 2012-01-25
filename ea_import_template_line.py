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

class ea_import_template_line(osv.osv):
    _name='ea_import.template.line'
    _columns = {
        'name' : fields.char('name',size=256),
        'template_id': fields.many2one('ea_import.template', 'Template',),
        'sequence': fields.integer('Sequence', required=True),
        'field_expression': fields.char('Target field expression', size=512, required=True),
        'field_type': fields.selection([
                                        ('text', 'text'),
                                        ('integer', 'integer'),
                                        ('float', 'float'),
                                        ('date', 'date'),
                                        ('datetime', 'datetime'),
                                        ('boolean', 'boolean'),
                                        ('many2one', 'many2one'),
                                       ], 'Field Type', required=True),
        'test_result_field': fields.char('Test Result', size=512,),
        'test_result_record_number': fields.integer('Record Number'),
        'create_new': fields.boolean('Create new?', ),
        'required': fields.boolean('Required', ),
        'header_column_name': fields.char('Header Column Name', size=64,),
        'time_format': fields.char('Time Format', size=128, help="""DIRECTIVE       MEANING
%a	Locale’s abbreviated weekday name.
%A	Locale’s full weekday name.
%b	Locale’s abbreviated month name.
%B	Locale’s full month name.
%c	Locale’s appropriate date and time representation.
%d	Day of the month as a decimal number [01,31].
%H	Hour (24-hour clock) as a decimal number [00,23].
%I	Hour (12-hour clock) as a decimal number [01,12].
%j	Day of the year as a decimal number [001,366].
%m	Month as a decimal number [01,12].
%M	Minute as a decimal number [00,59].
%p	Locale’s equivalent of either AM or PM.
%S	Second as a decimal number [00,61].
%U	Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.
%w	Weekday as a decimal number [0(Sunday),6].
%W	Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.
%x	Locale’s appropriate date representation.
%X	Locale’s appropriate time representation.
%y	Year without century as a decimal number [00,99].
%Y	Year with century as a decimal number.
%Z	Time zone name (no characters if no time zone exists).
%%	A literal '%' character.),"""),
        }

    _defaults = {
        'time_format': '%d/%m/%Y',
        'field_type': 'text',
    }

    def get_field(self, cr, uid, ids, input_string, context={}):
        for template_line in self.browse(cr, uid, ids, context=context):
            target_string = input_string.split(',')[template_line.sequence]
            template_line_type = template_line.field_type
            if template_line_type == 'text':
                return target_string
            elif template_line_type == 'integer':
                return int(target_string)
            elif template_line_type == 'float':
                return float(target_string)
            elif template_line_type == 'boolean':
                return bool(target_string)
            elif template_line_type == 'date':
                target_time = datetime.datetime.strptime(target_string, template_line.time_format)
                return target_time.strftime("%Y-%m-%d")
            elif template_line_type == 'datetime':
                target_time = datetime.datetime.strptime(target_string, template_line.time_format)
                return target_time.strftime("%Y-%m-%d %H:%M:%S")
            elif template_line_type == 'many2one':
                object_name, field_name = template_line.field_expression.split('/')
                target_obj_pool = self.pool.get(object_name)
                result = target_obj_pool.search(cr, uid, [(field_name, 'ilike', target_string)], context=context)
                if len(result) > 1:
                    raise osv.except_osv(_('Error !'), _("For %s relation and field (%s) there are more than 1 records (%d)" % (template_line.field_expression, target_string, len(result))))
                elif not result:
                    raise osv.except_osv(_('Error !'), _("There no field '%s' in %s relation" % (target_string, template_line.field_expression,)))
                else:
                    return result[0]

    def set_test_result_field(self, cr, uid, ids, context={}):
        for template_line in self.browse(cr, uid, ids, context=context):
            template_line.write({'test_result_field': template_line.get_field(template_line.template_id.get_string_by_number(template_line.test_result_record_number))})
        return True





ea_import_template_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
