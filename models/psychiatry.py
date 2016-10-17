#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api, exceptions, _
from openerp.tools.translate import _
import re
# from math import ceil
import logging
# from datetime import datetime
# from openerp.tools import email_split
# from math import floor
logger = logging.getLogger(__name__)
# import time

#################################################################################################################

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    patient= fields.Boolean(string=u'Paciente')
    insurer= fields.Boolean(string=u'EPS')

#################################################################################################################

class PsychiatryWhoqolbrefAnswer(models.Model):
    _name = 'psychiatry.whoqolbref.answer'

    name= fields.Char(string=u'Respuesta', size=25)
    answer_scale= fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                                    ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'),
                                    ('I', 'I'), ('J', 'J'), ('K', 'K')], string=u'Escala')
    measure= fields.Integer(string=u'Valor', size=1)

class PsychiatryWhoqolbrefQuestion(models.Model):
    _name = 'psychiatry.whoqolbref.question'

    name= fields.Char(string=u'Pregunta', size=150)
    category= fields.Selection([('G', 'General'), ('F', 'Salud física'),
                                ('P', 'Psicológica'), ('R', 'Relaciones interpersonales'),
                                ('E', 'Entorno')], string=u'Categoría')
    answer_scale= fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'),
                                    ('D', 'D'), ('E', 'E'), ('F', 'F')], string=u'Escala')
    active= fields.Boolean(string=u'Active', default=True)

class PsychiatryWhoqolbrefEvaluation(models.Model):
    _name = 'psychiatry.whoqolbref.evaluation'

    date_evaluation= fields.Date()
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

class PsychiatryWhoqolbrefQuestions(models.Model):
    _name = "psychiatry.whoqolbref.questions"

    evaluation_id= fields.Many2one('psychiatry.whoqolbref.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.whoqolbref.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.whoqolbref.answer', string=u'Respuesta')
    answer_measure= fields.Integer(related='answer_id.measure', store=True, string=u'Valor')

#################################################################################################################

class PsychiatryScl90rQuestion(models.Model):
    _name = 'psychiatry.scl90r.question'

    name= fields.Char(string=u'Pregunta', size=150)
    category= fields.Selection([('SOM', 'Somatizaciones'), ('OBS', 'Obsesiones y compulsiones'),
                                ('SI', 'Sensitividad interpersonal'), ('DEP', 'Depresión'),
                                ('ANS', 'Ansiedad'), ('HOS', 'Hostilidad'),
                                ('FOB', 'Ansiedad fóbica'), ('PAR', 'Ideación paranoide'),
                                ('PSIC', 'Psicoticismo'), ('IA', 'Ítems adicionales')], string=u'Dimensión')
    answer_scale= fields.Selection([('G', 'G')], string=u'Escala')
    active= fields.Boolean('Active', default=True)

class PsychiatryScl90rEvaluation(models.Model):
    _name = 'psychiatry.scl90r.evaluation'

    date_evaluation= fields.Date()
    question_ids= fields.One2many('psychiatry.scl90r.questions', 'evaluation_id')

    @api.onchange('date')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.scl90r.question']
        question_fill=[]
        for record in questions_pool.search([('active','=', 1)]):
            question_fill.append([0, 0,{'question_id': record.id}])
        self.question_ids = question_fill

class PsychiatryScl90rQuestions(models.Model):
    _name = "psychiatry.scl90r.questions"

    evaluation_id= fields.Many2one('psychiatry.scl90r.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.scl90r.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.whoqolbref.answer', string=u'Respuesta')
    answer_measure= fields.Integer(related='answer_id.measure', store=True, string=u'Valor')

#################################################################################################################

class PsychiatryMocaQuestion(models.Model):
    _name = 'psychiatry.moca.question'

    name= fields.Char(string=u'Pregunta', size=150)
    category= fields.Selection([('1', 'Alternancia conceptual'), ('2', 'Capacidades visuoconstructivas - Cubo'),
                                ('3', 'Capacidades visuoconstructivas - Reloj'), ('4', 'Denominación'),
                                ('5', 'Memoria'), ('6', 'Atención'),
                                ('7', 'Repetición de frases'), ('8', 'Fluidez verbal'),
                                ('9', 'Similitudes'), ('10', 'Recuerdo diferido'),
                                ('11', 'Orientación')], string=u'Dimensión')
    answer_scale= fields.Selection([('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K')], string=u'Escala')
    active= fields.Boolean('Active', default=True)

class PsychiatryMocaEvaluation(models.Model):
    _name = 'psychiatry.moca.evaluation'

    date_evaluation= fields.Date()
    question_ids= fields.One2many('psychiatry.moca.questions', 'evaluation_id')

    @api.onchange('date')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.moca.question']
        question_fill=[]
        for record in questions_pool.search([('active','=', 1)]):
            question_fill.append([0, 0,{'question_id': record.id}])
        self.question_ids = question_fill

class PsychiatryMocaQuestions(models.Model):
    _name = "psychiatry.moca.questions"

    evaluation_id= fields.Many2one('psychiatry.moca.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.moca.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.whoqolbref.answer', string=u'Respuesta')
    answer_measure= fields.Integer(related='answer_id.measure', store=True, string=u'Valor')

#################################################################################################################

class PsychiatryHospitalization(models.Model):
    _name = "psychiatry.hospitalization"

    date_in= fields.Date()
    patient_id= fields.Many2one('res.partner', string=u'Paciente')
    insurer_id= fields.Many2one('res.partner', string=u'EPS')
    evolutions_ids= fields.One2many('psychiatry.evolutions', 'hospitalization_id')
    review_ids= fields.One2many('psychiatry.review', 'hospitalization_id')

class PsychiatryEvolutions(models.Model):
    _name = "psychiatry.evolutions"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    date_evolution= fields.Date()
    comment= fields.Char(string=u'Observaciones')

class PsychiatryReview(models.Model):
    _name = "psychiatry.review"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    date_review= fields.Date()
    comment= fields.Char(string=u'Observaciones')
