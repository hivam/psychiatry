#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time

class psychiatry_whoqolbref_answer(osv.osv):
    _name = 'psychiatry.whoqolbref.answer'
    _rec_name = 'answer'
    _columns = {
        'answer_scale': fields.selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                          ('D', 'D'), ('E', 'E'), ('F', 'F')], 'Escala'),
        'answer': fields.char('Respuesta', size=25),
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
        'date': fields.date('Fecha', required=True),
        'question_ids': fields.one2many('psychiatry.whoqolbref.questions', 'evaluation_id', 'Preguntas'),
        }

    def _get_question_ids(self, cr, uid, context):
        ids = self.pool.get('psychiatry.whoqolbref.question').search(cr, uid, [], context=context)
        return ids

    _defaults = {
    'date': lambda *a: time.strftime('%Y-%m-%d'),
    'question_ids': _get_question_ids,
    }

psychiatry_whoqolbref_evaluation()

class psychiatry_whoqolbref_questions(osv.osv):
    _name = "psychiatry.whoqolbref.questions"
    _rec_name = 'evaluation_id'
    _columns = {
        'evaluation_id': fields.many2one('psychiatry.whoqolbref.evaluation', 'Evaluación', ondelete='cascade'),
        'question_id': fields.many2one('psychiatry.whoqolbref.question', 'Pregunta'),
        # 'answer_scale': fields.related('question_id', 'answer_scale', string="Escala", type="char", store=True),
        # 'answer_id': fields.many2one('psychiatry.whoqolbref.answer', 'Respuesta'),
        # 'answer_measure': fields.related('answer_id', 'measure', string="Valor", type="integer", store=True),
    }

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        rec_name = 'evaluation_id'
        res = [(r['id'], r[rec_name][1])
               for r in self.read(cr, uid, ids, [rec_name], context)]
        return res

    # def onchange_answer_scale(self, cr, uid, ids, question_id, context={}):
    #     values = {}
    #     if not question_id:
    #         return values
    #     question_answer_scale = self.pool.get('psychiatry.whoqolbref.question').browse(cr, uid, question_id, context=context)
    #     answer_scale_value = question_answer_scale.answer_scale
    #     values.update({
    #         'answer_scale': answer_scale_value,
    #     })
    #     return {'value': values}

    # def onchange_answer_measure(self, cr, uid, ids, answer_id, context={}):
    #     values = {}
    #     if not answer_id:
    #         return values
    #     answer_id_measure = self.pool.get('psychiatry.whoqolbref.answer').browse(cr, uid, answer_id, context=context)
    #     answer_scale_measure = answer_id_measure.measure
    #     values.update({
    #         'answer_measure': answer_scale_measure,
    #     })
    #     return {'value': values}

psychiatry_whoqolbref_questions()
