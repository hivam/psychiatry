#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api, exceptions, _
from openerp.tools.translate import _
# from math import ceil
import logging
# from datetime import datetime
# from openerp.tools import email_split
# from math import floor
logger = logging.getLogger(__name__)
# import time

class Psychiatry_Whoqolbref_Answer(models.Model):
    _name = 'psychiatry.whoqolbref.answer'

    name= fields.Char(string=u'Respuesta', size=25)
    answer_scale= fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                    ('D', 'D'), ('E', 'E'), ('F', 'F'),
                                    ('G', 'G')], string=u'Escala')
    measure= fields.Integer(string=u'Valor', size=1)

class Psychiatry_Whoqolbref_Question(models.Model):
    _name = 'psychiatry.whoqolbref.question'

    name= fields.Char(string=u'Pregunta', size=150)
    category= fields.Selection([('G', 'General'), ('F', 'Salud física'),
                                ('P', 'Psicológica'), ('R', 'Relaciones interpersonales'),
                                ('E', 'Entorno')], string=u'Categoría')
    answer_scale= fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                    ('D', 'D'), ('E', 'E'), ('F', 'F')], string=u'Escala')
    active= fields.Boolean('Active', default=True)

class psychiatry_whoqolbref_evaluation(models.Model):
    _name = 'psychiatry.whoqolbref.evaluation'

    date= fields.Date()
    question_ids= fields.One2many('psychiatry.whoqolbref.questions', 'evaluation_id')

    @api.onchange('date')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.whoqolbref.question']
        question_fill=[]
        for record in questions_pool.search([('active','=', 1)]):
            question_fill.append([0, 0,{'question_id': record.id}])
            # logger.info('##########################################')
            # logger.info(question_fill)
            # logger.info('##########################################')
        self.question_ids = question_fill

class Psychiatry_Whoqolbref_Questions(models.Model):
    _name = "psychiatry.whoqolbref.questions"

    evaluation_id= fields.Many2one('psychiatry.whoqolbref.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.whoqolbref.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.whoqolbref.answer', string=u'Respuesta')
    answer_measure= fields.Integer(related='answer_id.measure', store=True, string=u'Valor')

#################################################################################################################

class Psychiatry_Scl90r_Question(models.Model):
    _name = 'psychiatry.scl90r.question'

    name= fields.Char(string=u'Pregunta', size=150)
    category= fields.Selection([('SOM', 'Somatizaciones'), ('OBS', 'Obsesiones y compulsiones'),
                                ('SI', 'Sensitividad interpersonal'), ('DEP', 'Depresión'),
                                ('ANS', 'Ansiedad'), ('HOS', 'Hostilidad'),
                                ('FOB', 'Ansiedad fóbica'), ('PAR', 'Ideación paranoide'),
                                ('PSIC', 'Psicoticismo'), ('IA', 'Ítems adicionales')], string=u'Dimensión')
    answer_scale= fields.Selection([('G', 'G')], string=u'Escala')
    active= fields.Boolean('Active', default=True)

class psychiatry_Scl90r_evaluation(models.Model):
    _name = 'psychiatry.scl90r.evaluation'

    date= fields.Date()
    question_ids= fields.One2many('psychiatry.scl90r.questions', 'evaluation_id')

    @api.onchange('date')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.scl90r.question']
        question_fill=[]
        for record in questions_pool.search([('active','=', 1)]):
            question_fill.append([0, 0,{'question_id': record.id}])
        self.question_ids = question_fill

class Psychiatry_Scl90r_Questions(models.Model):
    _name = "psychiatry.scl90r.questions"

    evaluation_id= fields.Many2one('psychiatry.scl90r.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.scl90r.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.whoqolbref.answer', string=u'Respuesta')
    answer_measure= fields.Integer(related='answer_id.measure', store=True, string=u'Valor')
