#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api, exceptions, _
from openerp.tools.translate import _
# from math import ceil
# import logging
# from datetime import datetime
# from openerp.tools import email_split
# from math import floor
# logger = logging.getLogger(__name__)

# from openerp.osv import fields, osv
# from openerp.tools.translate import _
# import time

# class psychiatry_whoqolbref_answer(osv.osv):
class Psychiatry_Whoqolbref_Answer(models.Model):
    _name = 'psychiatry.whoqolbref.answer'
    # _rec_name = 'answer'
    # _columns = {
    name= fields.Char(string=u'Respuesta', size=25)
    answer_scale= fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                    ('D', 'D'), ('E', 'E'), ('F', 'F')], string=u'Escala')
    measure= fields.Integer(string=u'Valor', size=1)
        # }

# psychiatry_whoqolbref_answer()

# class psychiatry_whoqolbref_question(osv.osv):
class Psychiatry_Whoqolbref_Question(models.Model):
    _name = 'psychiatry.whoqolbref.question'
    # _rec_name = 'question'
    # _columns = {
    name= fields.Char(string=u'Pregunta', size=150)
    category= fields.Selection([('G', 'General'), ('F', 'Salud física'),
                                ('P', 'Psicológica'), ('R', 'Relaciones interpersonales'),
                                ('E', 'Entorno')], string=u'Categoría')
    answer_scale= fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                    ('D', 'D'), ('E', 'E'), ('F', 'F')], string=u'Escala')
    # active: fields.Boolean('Active'),
        # }

    # _defaults = {
    #     'active': 1,
    # }

# psychiatry_whoqolbref_question()

# class psychiatry_whoqolbref_evaluation(osv.osv):
class psychiatry_whoqolbref_evaluation(models.Model):
    _name = 'psychiatry.whoqolbref.evaluation'
    # _rec_name = 'date'
    # _columns = {
    # name = fields.Char(string=u'Referencia')
    date= fields.Date()
    question_ids= fields.One2many('psychiatry.whoqolbref.questions', 'evaluation_id')
        # }

    @api.onchange('date')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.whoqolbref.question']
        question_fill=[]
        for record in questions_pool.browse(self):
            question_fill.append([0, 0,{'question_ids': record.id}])
        self.question_ids = question_fill

    # def _get_question_ids(self, cr, uid, context):
    #     ids = self.pool.get('psychiatry.whoqolbref.question').search(cr, uid, [( 'active',  '=', 1)], context=context)
    #     return ids

    # _defaults = {
    # 'date': lambda *a: time.strftime('%Y-%m-%d'),
    # 'question_ids': _get_question_ids,
    # }

# psychiatry_whoqolbref_evaluation()

# class psychiatry_whoqolbref_questions(osv.osv):
class Psychiatry_Whoqolbref_Questions(models.Model):
    _name = "psychiatry.whoqolbref.questions"
    # _rec_name = 'evaluation_id'
    # _columns = {
    # name = fields.Char(string=u'Referencia'),
    evaluation_id= fields.Many2one('psychiatry.whoqolbref.evaluation')
    question_id= fields.Many2one('psychiatry.whoqolbref.question')
        # 'answer_scale': fields.related('question_id', 'answer_scale', string="Escala", type="char", store=True),
        # 'answer_id': fields.many2one('psychiatry.whoqolbref.answer', 'Respuesta'),
        # 'answer_measure': fields.related('answer_id', 'measure', string="Valor", type="integer", store=True),
    # }


    # def name_get(self, cr, uid, ids, context={}):
    #     if not len(ids):
    #         return []
    #     rec_name = 'evaluation_id'
    #     res = [(r['id'], r[rec_name][1])
    #            for r in self.read(cr, uid, ids, [rec_name], context)]
    #     return res

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

    # _defaults = {
    #     'evaluation_id': lambda self, cr, uid, context: context.get('evaluation_id', False),
    # }

# psychiatry_whoqolbref_questions()
