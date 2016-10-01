#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp.osv import fields, osv
from openerp.tools.translate import _

class psychiatry_whoqolbref_answer(osv.osv):
    _name = 'psychiatry.whoqolbref.answer'
    _columns = {
        # 'category': fields.selection([('G', 'General'), ('F', 'Salud física'),
        #                               ('P', 'Psicológica'), ('R', 'Relaciones interpersonales'),
        #                               ('E', 'Entorno')], 'Categoría'),
        'answer_scale': fields.selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                          ('D', 'D'), ('E', 'E'), ('F', 'F')], 'Escala'),
        'answer': fields.char('Respuesta', size=15),
        'measure': fields.integer('Valor', size=1),
        }

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        rec_name = 'answer'
        res = [(r['id'], r[rec_name][1])
               for r in self.read(cr, uid, ids, [rec_name], context)]
        return res

psychiatry_whoqolbref_answer()
