#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp.osv import fields, osv
from openerp.tools.translate import _

class psychiatry_whoqolbref_answer(osv.osv):
    _name = 'psychiatry.whoqolbref.answer'
    _rec_name = 'answer'
    _columns = {
        'answer_scale': fields.selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                          ('D', 'D'), ('E', 'E'), ('F', 'F')], 'Escala'),
        'answer': fields.char('Respuesta', size=15),
        'measure': fields.integer('Valor', size=1),
        }

psychiatry_whoqolbref_answer()

class psychiatry_whoqolbref_question(osv.osv):
    _name = 'psychiatry.whoqolbref.question'
    _rec_name = 'question'
    _columns = {
        'category': fields.selection([('G', 'General'), ('F', 'Salud física'),
                                      ('P', 'Psicológica'), ('R', 'Relaciones interpersonales'),
                                      ('E', 'Entorno')], 'Categoría'),
        'question': fields.char('Pregunta', size=150),
        'answer_scale': fields.selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                          ('D', 'D'), ('E', 'E'), ('F', 'F')], 'Escala'),
        }

psychiatry_whoqolbref_question()

class psychiatry_whoqolbref_evaluation(osv.osv):
    _name = 'psychiatry.whoqolbref.evaluation'
    _rec_name = 'date'
    _columns = {
        'date': fields.datetime('Fecha', required=True),
        'question_ids': fields.one2many('psychiatry.whoqolbref.questions', 'evaluation_id', 'Preguntas',
                                             ondelete='restrict'),
        }

psychiatry_whoqolbref_evaluation()

class psychiatry_whoqolbref_questions(osv.osv):
    _name = "psychiatry.whoqolbref.questions"
    _rec_name = 'evaluation_id'
    _columns = {
        'evaluation_id': fields.many2one('psychiatry.whoqolbref.evaluation', 'Evaluación'),
        'question_id': fields.many2one('psychiatry.whoqolbref.question', 'Pregunta', required=True,
                                           ondelete='restrict'),
        'answer_id': fields.many2one('psychiatry.whoqolbref.answer', 'Respuesta', required=True,
                                           ondelete='restrict'),
    }

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        rec_name = 'evaluation_id'
        res = [(r['id'], r[rec_name][1])
               for r in self.read(cr, uid, ids, [rec_name], context)]
        return res

psychiatry_whoqolbref_questions()
