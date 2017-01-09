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

    name = fields.Char(string=u'Número')
    date_evaluation= fields.Date(string=u'Fecha', default=fields.Date.today())
    patient_id= fields.Many2one('res.partner', string=u'Paciente')
    score_general= fields.Integer(compute='_score_whoqolbref', string=u'General')
    score_fisica= fields.Integer(compute='_score_whoqolbref', string=u'Salud física')
    score_psicologica= fields.Integer(compute='_score_whoqolbref', string=u'Psicológica')
    score_relaciones= fields.Integer(compute='_score_whoqolbref', string=u'Relaciones interpersonales')
    score_entorno= fields.Integer(compute='_score_whoqolbref', string=u'Entorno')
    question_ids= fields.One2many('psychiatry.whoqolbref.questions', 'evaluation_id')

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('whoqolbref.sequence')
            })
        return super(PsychiatryWhoqolbrefEvaluation, self).create(vals)

    @api.depends('question_ids.answer_measure')
    def _score_whoqolbref(self):
        for record in self:
            score_g = 0
            score_f = 0
            score_p = 0
            score_r = 0
            score_e = 0
            for line in record.question_ids:
                question_category = line.question_id.category
                if question_category == 'G':
                    score_g += line.answer_measure
                if question_category == 'F':
                    score_f += line.answer_measure
                if question_category == 'P':
                    score_p += line.answer_measure
                if question_category == 'R':
                    score_r += line.answer_measure
                if question_category == 'E':
                    score_e += line.answer_measure
                    # logger.info('##########################################')
                    # logger.info(score_general)
                    # logger.info('##########################################')
        record.score_general = score_g
        record.score_fisica = score_f
        record.score_psicologica = score_p
        record.score_relaciones = score_r
        record.score_entorno = score_e

    # @api.multi
    # @api.depends('name', 'bic')
    # def name_get(self):
    #     result = []
    #     for bank in self:
    #         name = bank.name + (bank.bic and (' - ' + bank.bic) or '')
    #         result.append((bank.id, name))
    #     return result

    # @api.model
    # def name_search(self, name, args=None, operator='ilike', limit=100):
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = ['|', ('bic', '=ilike', name + '%'), ('name', operator, name)]
    #         if operator in expression.NEGATIVE_TERM_OPERATORS:
    #             domain = ['&'] + domain
    #     banks = self.search(domain + args, limit=limit)
    #     return banks.name_get()

    @api.onchange('date_evaluation')
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

    name = fields.Char(string=u'Número')
    date_evaluation= fields.Date(string=u'Fecha', default=fields.Date.today())
    patient_id= fields.Many2one('res.partner', string=u'Paciente')
    score_somatizaciones= fields.Float(compute='_score_scl90r', string=u'Somatizaciones')
    score_obsesiones_compulsiones= fields.Float(compute='_score_scl90r', string=u'Obsesiones y compulsiones')
    score_sensitividad_interpersonal= fields.Float(compute='_score_scl90r', string=u'Sensitividad interpersonal')
    score_depresion= fields.Float(compute='_score_scl90r', string=u'Depresión')
    score_ansiedad= fields.Float(compute='_score_scl90r', string=u'Ansiedad')
    score_hostilidad= fields.Float(compute='_score_scl90r', string=u'Hostilidad')
    score_ansiedad_fobica= fields.Float(compute='_score_scl90r', string=u'Ansiedad fóbica')
    score_ideacion_paranoide= fields.Float(compute='_score_scl90r', string=u'Ideación paranoide')
    score_psicoticismo= fields.Float(compute='_score_scl90r', string=u'Psicoticismo')
    score_items_adicionales= fields.Float(compute='_score_scl90r', string=u'Ítems adicionales')
    question_ids= fields.One2many('psychiatry.scl90r.questions', 'evaluation_id')

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('scl90r.sequence')
            })
        return super(PsychiatryScl90rEvaluation, self).create(vals)

    @api.depends('question_ids.answer_measure')
    def _score_scl90r(self):
        for record in self:
            # num_lineas = 0
            # score = 0
            score_som = 0
            score_obs = 0
            score_si = 0
            score_dep = 0
            score_ans = 0
            score_hos = 0
            score_fob = 0
            score_par = 0
            score_psic = 0
            score_ia = 0
            for line in record.question_ids:
                question_category = line.question_id.category
                if question_category == 'SOM':
                    score_som += line.answer_measure
                # and line.answer_measure != False:
                    # num_lineas += 1
                #     score += line.answer_measure
                # if num_lineas > 0:
                    # score_som = score/num_lineas
                    # logger.info('##########################################')
                    # logger.info(score_som)
                    # logger.info('##########################################')
                if question_category == 'OBS':
                    score_obs += line.answer_measure
                if question_category == 'SI':
                    score_si += line.answer_measure
                if question_category == 'DEP':
                    score_dep += line.answer_measure
                if question_category == 'ANS':
                    score_ans += line.answer_measure
                if question_category == 'HOS':
                    score_hos += line.answer_measure
                if question_category == 'FOB':
                    score_fob += line.answer_measure
                if question_category == 'PAR':
                    score_par += line.answer_measure
                if question_category == 'PSIC':
                    score_psic += line.answer_measure
                if question_category == 'IA':
                    score_ia += line.answer_measure
        record.score_somatizaciones = score_som
        record.score_obsesiones_compulsiones = score_obs
        record.score_sensitividad_interpersonal = score_si
        record.score_depresion = score_dep
        record.score_ansiedad = score_ans
        record.score_hostilidad = score_hos
        record.score_ansiedad_fobica = score_fob
        record.score_ideacion_paranoide = score_par
        record.score_psicoticismo = score_psic
        record.score_items_adicionales = score_ia

    @api.onchange('date_evaluation')
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

    name = fields.Char(string=u'Número')
    date_evaluation= fields.Date(string=u'Fecha', default=fields.Date.today())
    patient_id= fields.Many2one('res.partner', string=u'Paciente')
    question_ids= fields.One2many('psychiatry.moca.questions', 'evaluation_id')

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('moca.sequence')
            })
        return super(PsychiatryMocaEvaluation, self).create(vals)

    @api.onchange('date_evaluation')
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

class PsychiatrySpa(models.Model):
    _name = 'psychiatry.spa'

    name= fields.Char(string=u'Sustancia psicoactiva', size=150)

class PsychiatryDrug(models.Model):
    _name = 'psychiatry.drug'

    name= fields.Char(string=u'Medicamento', size=150)

class PsychiatryDiseases(models.Model):
    _name = 'psychiatry.diseases'

    code_dx= fields.Char(string=u'Código', size=4)
    name= fields.Char(string=u'Diagnóstico', size=256)
    psychiatry= fields.Boolean('Dx Psiquiatría')
    vts= fields.Boolean('Dx Virus de Transmisión Sanguínea - VTS')

class PsychiatryHospitalization(models.Model):
    _name = "psychiatry.hospitalization"

    name = fields.Char(string=u'Número')
    date_in= fields.Date(string=u'Fecha de ingreso', default=fields.Date.today())
    patient_id= fields.Many2one('res.partner', string=u'Paciente')
    insurer_id= fields.Many2one('res.partner', string=u'EPS')
    compromise_patient_in= fields.Selection([('0', 'Ninguno'), ('1', 'Poco'), ('2', 'Medio'), ('3', 'Alto')], string=u'Nivel de compromiso al ingreso - Paciente')
    compromise_clinic_in= fields.Selection([('0', 'Ninguno'), ('1', 'Poco'), ('2', 'Medio'), ('3', 'Alto')], string=u'Nivel de compromiso al ingreso - Clínico')
    date_out= fields.Date(string=u'Fecha de egreso')
    type_out= fields.Selection([('1', 'Planificado'), ('2', 'Alta Voluntaria'), ('3', 'Evasión'),
                                ('4', 'Recaída'), ('5', 'Otro imprevisto')], string=u'Tipo de egreso')
    place_out= fields.Selection([('1', 'Ninguno'), ('2', 'Comunidad Terapéutica'), ('3', 'Ambulatorio'),
                                ('4', 'Hospital Día'), ('5', 'Otro')], string=u'Direccionado a')
    spa_ids= fields.One2many('psychiatry.spa.consume', 'hospitalization_id')
    drug_ids_in= fields.One2many('psychiatry.drugs.in', 'hospitalization_id')
    drug_ids_out= fields.One2many('psychiatry.drugs.out', 'hospitalization_id')
    vts_id= fields.Many2one('psychiatry.diseases', string=u'Virus de Transmisión Sanguínea - VTS')
    diseases_psychiatry_ids= fields.One2many('psychiatry.diseases.psychiatry', 'hospitalization_id')
    diseases_others_ids= fields.One2many('psychiatry.diseases.others', 'hospitalization_id')
    evolutions_ids= fields.One2many('psychiatry.evolutions', 'hospitalization_id')
    review_ids= fields.One2many('psychiatry.review', 'hospitalization_id')
    compromise_patient_out= fields.Selection([('0', 'Ninguno'), ('1', 'Poco'), ('2', 'Medio'), ('3', 'Alto')], string=u'Nivel de compromiso al egreso - Paciente')
    compromise_clinic_out= fields.Selection([('0', 'Ninguno'), ('1', 'Poco'), ('2', 'Medio'), ('3', 'Alto')], string=u'Nivel de compromiso al egreso - Clínico')
    leave_ids= fields.One2many('psychiatry.leaves', 'hospitalization_id')

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('hospitalization.sequence')
            })
        return super(PsychiatryHospitalization, self).create(vals)

class PsychiatrySpaConsume(models.Model):
    _name = "psychiatry.spa.consume"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    spa_id= fields.Many2one('psychiatry.spa', string=u'SPA')

class PsychiatryDrugsIn(models.Model):
    _name = "psychiatry.drugs.in"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    drug_id= fields.Many2one('psychiatry.drug', string=u'Medicamento')

class PsychiatryDrugsOut(models.Model):
    _name = "psychiatry.drugs.out"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    drug_id= fields.Many2one('psychiatry.drug', string=u'Medicamento')

class PsychiatryDiseasesPsychiatry(models.Model):
    _name = "psychiatry.diseases.psychiatry"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    diseases_id= fields.Many2one('psychiatry.diseases', string=u'Patología')
    diseases_type= fields.Selection([('1', 'Nuevo'), ('2', 'Antiguo')], string=u'Tipo')

class PsychiatryDiseasesOthers(models.Model):
    _name = "psychiatry.diseases.others"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    diseases_id= fields.Many2one('psychiatry.diseases', string=u'Patología')
    diseases_type= fields.Selection([('1', 'Nuevo'), ('2', 'Antiguo')], string=u'Tipo')

class PsychiatryEvolutions(models.Model):
    _name = "psychiatry.evolutions"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    date_evolution= fields.Date(default=fields.Date.today())
    comment= fields.Char(string=u'Observaciones')

class PsychiatryReview(models.Model):
    _name = "psychiatry.review"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    date_review= fields.Date(default=fields.Date.today())
    comment= fields.Char(string=u'Observaciones')

class PsychiatryLeaves(models.Model):
    _name = "psychiatry.leaves"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    date_leave= fields.Date(default=fields.Date.today())
    leave_type= fields.Selection([('1', 'Ninguno'), ('2', 'Día Completo'), ('3', 'Medio día'), ('4', 'Salida - Visita')], string=u'Tipo')
