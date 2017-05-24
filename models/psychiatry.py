#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api, exceptions, _
from openerp.tools.translate import _
import re
# from math import ceil
import logging
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# from openerp.tools import email_split
# from math import floor
logger = logging.getLogger(__name__)
# import time#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


#################################################################################################################

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    patient= fields.Boolean(string=u'Paciente', default=True)
    insurer= fields.Boolean(string=u'EPS')
    document_type= fields.Selection ([('12','Tarjeta de identidad'),
                                  ('13','Cédula de ciudadanía'),
                                  ('21','Tarjeta de extranjería'),
                                  ('22','Cédula de extranjería'),
                                  ('31','NIT'),
                                  ('41','Pasaporte'),
                                  ('42','Documento de identificación extranjero'),
                                  ('43','Sin identificación del exterior o para uso definido por la DIAN')],
                                  string=u'Tipo de Documento')
    num_doc = fields.Char(string=u'Número de documento')
    whoqolbref_count= fields.Integer(compute='_count_whoqolbref', string=u'WHOQOL-BREF')
    whoqolbref_ids= fields.One2many('psychiatry.whoqolbref.evaluation','patient_id','WHOQOL-BREF')
    scl90r_count= fields.Integer(compute='_count_scl90r', string=u'SCL-90-R')
    scl90r_ids= fields.One2many('psychiatry.scl90r.evaluation','patient_id','SCL-90-R')
    moca_count= fields.Integer(compute='_count_moca', string=u'MoCa')
    moca_ids= fields.One2many('psychiatry.moca.evaluation','patient_id','MoCa')
    sf36_count= fields.Integer(compute='_count_sf36', string=u'SF-36')
    sf36_ids= fields.One2many('psychiatry.sf36.evaluation','patient_id','SF-36')
    hospitalization_count= fields.Integer(compute='_count_hospitalization', string=u'Ingresos')
    hospitalization_ids= fields.One2many('psychiatry.hospitalization','patient_id','Ingresos')
    sex = fields.Selection([('M','Masculino'), ('F','Femenino')], string=u'Sexo')


    @api.depends('whoqolbref_ids')
    def _count_whoqolbref(self):
        for record in self:
            record.whoqolbref_count = len(record.whoqolbref_ids)

    @api.depends('scl90r_ids')
    def _count_scl90r(self):
        for record in self:
            record.scl90r_count = len(record.scl90r_ids)

    @api.depends('moca_ids')
    def _count_moca(self):
        for record in self:
            record.moca_count = len(record.moca_ids)

    @api.depends('hospitalization_ids')
    def _count_hospitalization(self):
        for record in self:
            record.hospitalization_count = len(record.hospitalization_ids)

    @api.depends('sf36_ids')
    def _count_sf36(self):
        for record in self:
            record.sf36_count = len(record.sf36_ids)



#################################################################################################################

class PsychiatryAnswer(models.Model):
    _name = 'psychiatry.answer'

    name= fields.Char(string=u'Respuesta', size=35)
    answer_scale= fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                                    ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'),
                                    ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'),
                                    ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'),
                                    ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'),
                                    ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'),
                                    ('Y', 'Y')], string=u'Escala')
    measure= fields.Integer(string=u'Valor', size=3)



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
    date_evaluation= fields.Date(string=u'Fecha', default=fields.Date.today(), required=True)
    patient_id= fields.Many2one('res.partner', string=u'Paciente', required=True)
    score_general= fields.Integer(compute='_score_whoqolbref', string=u'General')
    score_fisica= fields.Integer(compute='_score_whoqolbref', string=u'Salud física')
    score_psicologica= fields.Integer(compute='_score_whoqolbref', string=u'Psicológica')
    score_relaciones= fields.Integer(compute='_score_whoqolbref', string=u'Relaciones interpersonales')
    score_entorno= fields.Integer(compute='_score_whoqolbref', string=u'Entorno')
    question_ids= fields.One2many('psychiatry.whoqolbref.questions', 'evaluation_id')
    category_id= fields.Many2many(related='patient_id.category_id', store=True, string='Etiqueta')
    sex = fields.Selection(related='patient_id.sex', store=True, string='Sexo')
    age = fields.Integer(compute='_age_evaluation', string="Edad", store=True)
    rango_edad= fields.Many2one('psychiatry.rango.edad', string='Rango de edad')

    @api.depends('patient_id.birth_date', 'date_evaluation')
    def _age_evaluation(self):

        if self.patient_id.birth_date and self.date_evaluation:
            d1 = datetime.strptime(self.patient_id.birth_date, "%Y-%m-%d").date()
            d2 = datetime.strptime(self.date_evaluation, "%Y-%m-%d").date()
            self.age = relativedelta(d2, d1).years

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

        record.score_general = score_g
        record.score_fisica = score_f
        record.score_psicologica = score_p
        record.score_relaciones = score_r
        record.score_entorno = score_e

    @api.onchange('date_evaluation')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.whoqolbref.question']
        question_fill=[]
        for record in questions_pool.search([('active','=', 1)]):
            question_fill.append([0, 0,{'question_id': record.id}])
        self.question_ids = question_fill

    @api.onchange('age')
    def _onchange_rango_edad(self):
        rango_id = []
        for record in self:
            if record.age:
                rango_id = self.env['psychiatry.rango.edad'].search([('rango_inic','<=', record.age), ('rango_fin','>=', record.age)], limit=1)
                rango_id = rango_id.id
            logger.info('rangoedad')
            logger.info(rango_id)
        self.rango_edad = rango_id

class PsychiatryWhoqolbrefQuestions(models.Model):
    _name = "psychiatry.whoqolbref.questions"

    evaluation_id= fields.Many2one('psychiatry.whoqolbref.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.whoqolbref.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.answer', string=u'Respuesta')
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
    date_evaluation= fields.Date(string=u'Fecha', default=fields.Date.today(), required=True)
    patient_id= fields.Many2one('res.partner', string=u'Paciente', required=True)
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
    score_severidad= fields.Float(compute='_score_scl90r', string=u'Índice global de severidad')
    score_sintomas_positivos= fields.Float(compute='_score_scl90r', string=u'Total síntomas positivos')
    score_malestar_positivo= fields.Float(compute='_score_scl90r', string=u'Indice de Malestar Sintomático Positivo')
    question_ids= fields.One2many('psychiatry.scl90r.questions', 'evaluation_id')
    category_id= fields.Many2many(related='patient_id.category_id', store=True, string='Etiqueta')
    sex = fields.Selection(related='patient_id.sex', store=True, string='Sexo')
    age = fields.Integer(compute='_age_evaluation', string="Edad", store=True)
    rango_edad= fields.Many2one('psychiatry.rango.edad', string='Rango de edad')

    @api.depends('patient_id.birth_date', 'date_evaluation')
    def _age_evaluation(self):

        if self.patient_id.birth_date and self.date_evaluation:
            d1 = datetime.strptime(self.patient_id.birth_date, "%Y-%m-%d").date()
            d2 = datetime.strptime(self.date_evaluation, "%Y-%m-%d").date()
            self.age = relativedelta(d2, d1).years


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
            score_som = 0
            num_lineas_som = 0
            score_obs = 0
            num_lineas_obs = 0
            score_si = 0
            num_lineas_si = 0
            score_dep = 0
            num_lineas_dep = 0
            score_ans = 0
            num_lineas_ans = 0
            score_hos = 0
            num_lineas_hos = 0
            score_fob = 0
            num_lineas_fob = 0
            score_par = 0
            num_lineas_par = 0
            score_psic = 0
            num_lineas_psic = 0
            score_ia = 0
            num_lineas_ia = 0
            num_lineas_sp = 0
            malestar_sintomatico_positivo = 0

            for line in record.question_ids:
                question_category = line.question_id.category
                answer_exist = line.answer_id
                answer_score = line.answer_measure
                if question_category == 'SOM' and answer_exist:
                    score_som += float(line.answer_measure)
                    num_lineas_som += 1
                if question_category == 'OBS' and answer_exist:
                    score_obs += float(line.answer_measure)
                    num_lineas_obs += 1
                if question_category == 'SI' and answer_exist:
                    score_si += float(line.answer_measure)
                    num_lineas_si += 1
                if question_category == 'DEP' and answer_exist:
                    score_dep += float(line.answer_measure)
                    num_lineas_dep += 1
                if question_category == 'ANS' and answer_exist:
                    score_ans += float(line.answer_measure)
                    num_lineas_ans += 1
                if question_category == 'HOS' and answer_exist:
                    score_hos += float(line.answer_measure)
                    num_lineas_hos += 1
                if question_category == 'FOB' and answer_exist:
                    score_fob += float(line.answer_measure)
                    num_lineas_fob += 1
                if question_category == 'PAR' and answer_exist:
                    score_par += float(line.answer_measure)
                    num_lineas_par += 1
                if question_category == 'PSIC' and answer_exist:
                    score_psic += float(line.answer_measure)
                    num_lineas_psic += 1
                if question_category == 'IA' and answer_exist:
                    score_ia += float(line.answer_measure)
                    num_lineas_ia += 1
                if answer_exist and (answer_score > 0):
                    num_lineas_sp += 1

        if num_lineas_som == 0:
            num_lineas_som = 1
        if num_lineas_obs == 0:
            num_lineas_obs = 1
        if num_lineas_si == 0:
            num_lineas_si = 1
        if num_lineas_dep == 0:
            num_lineas_dep = 1
        if num_lineas_ans == 0:
            num_lineas_ans = 1
        if num_lineas_hos == 0:
            num_lineas_hos = 1
        if num_lineas_fob == 0:
            num_lineas_fob = 1
        if num_lineas_par == 0:
            num_lineas_par = 1
        if num_lineas_psic == 0:
            num_lineas_psic = 1
        if num_lineas_ia == 0:
            num_lineas_ia = 1

        score_total = float(score_som + score_obs + score_si + score_dep + score_ans +
                            score_hos + score_fob + score_par + score_psic + score_ia)
        num_lineas_total = float(num_lineas_som + num_lineas_obs + num_lineas_si + num_lineas_dep + num_lineas_ans +
                                 num_lineas_hos + num_lineas_fob + num_lineas_par + num_lineas_psic + num_lineas_ia)

        if num_lineas_total == 0:
            num_lineas_total = 1

        if num_lineas_sp > 0:
            malestar_sintomatico_positivo = float(score_total/num_lineas_sp)

        # logger.info('##########################################')
        # logger.info(score_total)
        # logger.info(num_lineas_total)
        # logger.info('##########################################')

        record.score_somatizaciones = float(score_som/num_lineas_som)
        record.score_obsesiones_compulsiones = float(score_obs/num_lineas_obs)
        record.score_sensitividad_interpersonal = float(score_si/num_lineas_si)
        record.score_depresion = float(score_dep/num_lineas_dep)
        record.score_ansiedad = float(score_ans/num_lineas_ans)
        record.score_hostilidad = float(score_hos/num_lineas_hos)
        record.score_ansiedad_fobica = float(score_fob/num_lineas_fob)
        record.score_ideacion_paranoide = float(score_par/num_lineas_par)
        record.score_psicoticismo = float(score_psic/num_lineas_psic)
        record.score_items_adicionales = float(score_ia)
        record.score_severidad = float(score_total/num_lineas_total)
        record.score_sintomas_positivos = float(num_lineas_sp)
        record.score_malestar_positivo = float(malestar_sintomatico_positivo)

    @api.onchange('date_evaluation')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.scl90r.question']
        question_fill=[]
        for record in questions_pool.search([('active','=', 1)]):
            question_fill.append([0, 0,{'question_id': record.id}])
        self.question_ids = question_fill

    @api.onchange('age')
    def _onchange_rango_edad(self):
        rango_id = []
        for record in self:
            if record.age:
                rango_id = self.env['psychiatry.rango.edad'].search([('rango_inic','<=', record.age), ('rango_fin','>=', record.age)], limit=1)
                rango_id = rango_id.id
            logger.info('rangoedad')
            logger.info(rango_id)
        self.rango_edad = rango_id


class PsychiatryScl90rQuestions(models.Model):
    _name = "psychiatry.scl90r.questions"

    evaluation_id= fields.Many2one('psychiatry.scl90r.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.scl90r.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.answer', string=u'Respuesta')
    answer_measure= fields.Integer(related='answer_id.measure', store=True, string=u'Valor')

#################################################################################################################

class PsychiatryMocaQuestion(models.Model):
    _name = 'psychiatry.moca.question'

    name= fields.Char(string=u'Pregunta', size=150)
    category= fields.Selection([('1', 'Alternancia conceptual'), ('2', 'Capacidades visuoconstructivas - Cubo'),
                                ('3A', 'Capacidades visuoconstructivas - Reloj - Contorno'), ('3B', 'Capacidades visuoconstructivas - Reloj - Números'),
                                ('3C', 'Capacidades visuoconstructivas - Reloj - Agujas'), ('4', 'Denominación'),
                                ('5', 'Memoria'), ('6', 'Atención'),
                                ('7', 'Repetición de frases'), ('8', 'Fluidez verbal'),
                                ('9', 'Similitudes'), ('10', 'Recuerdo diferido'),
                                ('11', 'Orientación')], string=u'Dimensión')
    answer_scale= fields.Selection([('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L')], string=u'Escala')
    active= fields.Boolean('Active', default=True)

class PsychiatryMocaEvaluation(models.Model):
    _name = 'psychiatry.moca.evaluation'

    name = fields.Char(string=u'Número')
    date_evaluation= fields.Date(string=u'Fecha', default=fields.Date.today(), required=True)
    patient_id= fields.Many2one('res.partner', string=u'Paciente', required=True)
    score_moca= fields.Float(compute='_score_moca', string=u'Puntuación final')
    question_ids= fields.One2many('psychiatry.moca.questions', 'evaluation_id')
    category_id= fields.Many2many(related='patient_id.category_id', store=True, string='Etiqueta')
    sex = fields.Selection(related='patient_id.sex', store=True, string='Sexo')
    age = fields.Integer(compute='_age_evaluation', string="Edad", store=True)
    rango_edad= fields.Many2one('psychiatry.rango.edad', string='Rango de edad')

    @api.depends('patient_id.birth_date', 'date_evaluation')
    def _age_evaluation(self):

        if self.patient_id.birth_date and self.date_evaluation:
            d1 = datetime.strptime(self.patient_id.birth_date, "%Y-%m-%d").date()
            d2 = datetime.strptime(self.date_evaluation, "%Y-%m-%d").date()
            self.age = relativedelta(d2, d1).years

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('moca.sequence')
            })
        return super(PsychiatryMocaEvaluation, self).create(vals)

    @api.depends('question_ids.answer_measure')
    def _score_moca(self):
        for record in self:
            score_cubo = 0
            score_numeros = 0
            score_agujas = 0
            score_resto = 0

            for line in record.question_ids:
                question_category = line.question_id.category
                # answer_exist = line.answer_id
                # answer_score = line.answer_measure
                if question_category == '2':
                    score_cubo += float(line.answer_measure)
                elif question_category == '3B':
                    score_numeros += float(line.answer_measure)
                elif question_category == '3C':
                    score_agujas += float(line.answer_measure)
                else:
                    score_resto += float(line.answer_measure)

        if score_cubo == 6:
            score_cubo = 1
        else:
            score_cubo = 0

        if score_numeros == 4:
            score_numeros = 1
        else:
            score_numeros = 0

        if score_agujas == 3:
            score_agujas = 1
        else:
            score_agujas = 0

        record.score_moca = float(score_cubo + score_numeros + score_agujas + score_resto)

    @api.onchange('date_evaluation')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.moca.question']
        question_fill=[]
        for record in questions_pool.search([('active','=', 1)]):
            question_fill.append([0, 0,{'question_id': record.id}])
        self.question_ids = question_fill
        
    @api.onchange('age')
    def _onchange_rango_edad(self):
        rango_id = []
        for record in self:
            if record.age:
                rango_id = self.env['psychiatry.rango.edad'].search([('rango_inic','<=', record.age), ('rango_fin','>=', record.age)], limit=1)
                rango_id = rango_id.id
            logger.info('rangoedad')
            logger.info(rango_id)
        self.rango_edad = rango_id

class PsychiatryMocaQuestions(models.Model):
    _name = "psychiatry.moca.questions"

    evaluation_id= fields.Many2one('psychiatry.moca.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.moca.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.answer', string=u'Respuesta')
    answer_measure= fields.Integer(related='answer_id.measure', store=True, string=u'Valor')

#################################################################################################################
#################################################################################################################

class PsychiatrySf36Question(models.Model):
    _name = 'psychiatry.sf36.question'

    name= fields.Char(string=u'Pregunta', size=200)
    category= fields.Selection([('FF', 'Función Física'), ('RF', 'Rol Físico'),
                                ('DC', 'Dolor Corporal'), ('SG', 'Salud General'),
                                ('VI', 'Vitalidad'), ('FS', 'Función Social'),
                                ('RE', 'Rol Emocional'), ('SM', 'Salud Mental'),
                                ('SMR', 'Salud Mental'), ('SFR', 'Salud Física')], string=u'Dimensión')
    answer_scale= fields.Selection([('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'),
                                    ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'),
                                    ('W', 'W'), ('X', 'X'), ('Y', 'Y')], string=u'Escala')
    active= fields.Boolean('Active', default=True)

class PsychiatrySf36Evaluation(models.Model):
    _name = 'psychiatry.sf36.evaluation'

    name = fields.Char(string=u'Número')
    date_evaluation= fields.Date(string=u'Fecha', default=fields.Date.today(), required=True)
    patient_id= fields.Many2one('res.partner', string=u'Paciente', required=True)
    score_funcion_fisica= fields.Float(compute='_score_sf36', string=u'Función Física')
    score_rol_fisico= fields.Float(compute='_score_sf36', string=u'Rol Físico')
    score_dolor_corporal= fields.Float(compute='_score_sf36', string=u'Dolor Corporal')
    score_salud_general= fields.Float(compute='_score_sf36', string=u'Salud General')
    score_vitalidad= fields.Float(compute='_score_sf36', string=u'Vitalidad')
    score_funcion_social= fields.Float(compute='_score_sf36', string=u'Función Social')
    score_rol_emocional= fields.Float(compute='_score_sf36', string=u'Rol Emocional')
    score_salud_mental= fields.Float(compute='_score_sf36', string=u'Salud Mental')
    score_salud_fisica_rs= fields.Float(compute='_score_sf36', string=u'Salud Física')
    score_salud_mental_rs= fields.Float(compute='_score_sf36', string=u'Salud Mental')
    question_ids= fields.One2many('psychiatry.sf36.questions', 'evaluation_id')
    category_id= fields.Many2many(related='patient_id.category_id', store=True, string='Etiqueta')
    sex = fields.Selection(related='patient_id.sex', store=True, string='Sexo')
    age = fields.Integer(compute='_age_evaluation', string="Edad", store=True)
    rango_edad= fields.Many2one('psychiatry.rango.edad', string='Rango de edad')

    @api.depends('patient_id.birth_date', 'date_evaluation')
    def _age_evaluation(self):

        if self.patient_id.birth_date and self.date_evaluation:
            d1 = datetime.strptime(self.patient_id.birth_date, "%Y-%m-%d").date()
            d2 = datetime.strptime(self.date_evaluation, "%Y-%m-%d").date()
            self.age = relativedelta(d2, d1).years

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('sf36.sequence')
            })
        return super(PsychiatrySf36Evaluation, self).create(vals)

    @api.depends('question_ids.answer_measure')
    def _score_sf36(self):
        for record in self:
            score_ff = 0
            num_lineas_ff = 0
            score_rf = 0
            num_lineas_rf = 0
            score_dc = 0
            num_lineas_dc = 0
            score_sg = 0
            num_lineas_sg = 0
            score_vi = 0
            num_lineas_vi = 0
            score_fs = 0
            num_lineas_fs = 0
            score_re = 0
            num_lineas_re = 0
            score_sm = 0
            num_lineas_sm = 0
            score_rs = 0
            num_lineas_rs = 0
            score_sfr = 0
            num_lineas_sfr = 0
            score_smr = 0
            num_lineas_smr = 0

            for line in record.question_ids:
                question_category = line.question_id.category
                answer_exist = line.answer_id
                answer_score = line.answer_measure
                if question_category == 'FF' and answer_exist:
                    score_ff += float(line.answer_measure)
                    num_lineas_ff += 1
                if question_category == 'RF' and answer_exist:
                    score_rf += float(line.answer_measure)
                    num_lineas_rf += 1
                if question_category == 'DC' and answer_exist:
                    score_dc += float(line.answer_measure)
                    num_lineas_dc += 1
                if question_category == 'SG' and answer_exist:
                    score_sg += float(line.answer_measure)
                    num_lineas_sg += 1
                if question_category == 'VI' and answer_exist:
                    score_vi += float(line.answer_measure)
                    num_lineas_vi += 1
                if question_category == 'FS' and answer_exist:
                    score_fs += float(line.answer_measure)
                    num_lineas_fs += 1
                if question_category == 'RE' and answer_exist:
                    score_re += float(line.answer_measure)
                    num_lineas_re += 1
                if question_category == 'SM' and answer_exist:
                    score_sm += float(line.answer_measure)
                    num_lineas_sm += 1
                if answer_exist and (answer_score > 0):
                    num_lineas_rs += 1

        if num_lineas_ff == 0:
            num_lineas_ff = 1
        if num_lineas_rf == 0:
            num_lineas_rf = 1
        if num_lineas_dc == 0:
            num_lineas_dc = 1
        if num_lineas_sg == 0:
            num_lineas_sg = 1
        if num_lineas_vi == 0:
            num_lineas_vi = 1
        if num_lineas_fs == 0:
            num_lineas_fs = 1
        if num_lineas_re == 0:
            num_lineas_re = 1
        if num_lineas_sm == 0:
            num_lineas_sm = 1
        if num_lineas_sfr == 0:
            num_lineas_sfr = 1
        if num_lineas_smr == 0:
            num_lineas_smr = 1
        if num_lineas_rs == 0:
            num_lineas_rs = 1

        score_total = float(score_ff + score_rf + score_dc + score_sg + score_vi +
                            score_fs + score_re + score_sm)
        score_sfr = float(score_ff + score_rf + score_dc + score_sg)
        score_smr = float(score_vi + score_fs + score_re + score_sm)

        num_lineas_total = float(num_lineas_ff + num_lineas_rf + num_lineas_dc + num_lineas_sg + num_lineas_vi +
                                 num_lineas_fs + num_lineas_re + num_lineas_sm)

        if num_lineas_total == 0:
            num_lineas_total = 1


        # logger.info('##########################################')
        # logger.info(score_total)
        # logger.info(num_lineas_total)
        # logger.info('##########################################')

        record.score_funcion_fisica = float(score_ff/num_lineas_ff)
        record.score_rol_fisico = float(score_rf/num_lineas_rf)
        record.score_dolor_corporal = float(score_dc/num_lineas_dc)
        record.score_salud_general = float(score_sg/num_lineas_sg)
        record.score_vitalidad = float(score_vi/num_lineas_vi)
        record.score_funcion_social = float(score_fs/num_lineas_fs)
        record.score_rol_emocional = float(score_re/num_lineas_re)
        record.score_salud_mental = float(score_sm/num_lineas_sm)
        record.score_salud_fisica_rs = float(score_sfr/num_lineas_rs)
        record.score_salud_mental_rs = float(score_smr/num_lineas_total)


    @api.onchange('date_evaluation')
    def _onchange_date(self):
        questions_pool = self.env['psychiatry.sf36.question']
        question_fill=[]
        for record in questions_pool.search([('active','=', 1)]):
            question_fill.append([0, 0,{'question_id': record.id}])
        self.question_ids = question_fill

    @api.onchange('age')
    def _onchange_rango_edad(self):
        rango_id = []
        for record in self:
            if record.age:
                rango_id = self.env['psychiatry.rango.edad'].search([('rango_inic','<=', record.age), ('rango_fin','>=', record.age)], limit=1)
                rango_id = rango_id.id
            logger.info('rangoedad')
            logger.info(rango_id)
        self.rango_edad = rango_id

class PsychiatrySf36Questions(models.Model):
    _name = "psychiatry.sf36.questions"

    evaluation_id= fields.Many2one('psychiatry.sf36.evaluation', ondelete='cascade')
    question_id= fields.Many2one('psychiatry.sf36.question', string=u'Pregunta')
    answer_scale= fields.Selection(related='question_id.answer_scale', store=True)
    answer_id= fields.Many2one('psychiatry.answer', string=u'Respuesta')
    answer_measure= fields.Integer(related='answer_id.measure', store=True, string=u'Valor')


#################################################################################################################

class PsychiatryRangoEdad(models.Model):
    _name = 'psychiatry.rango.edad'

    name = fields.Char(string=u'Etapa del ciclo de vida')
    rango_inic = fields.Integer(string=u'Rango Inicial')
    rango_fin = fields.Integer(string=u'Rango Final')

#################################################################################################################
#################################################################################################################

class PsychiatrySpa(models.Model):
    _name = 'psychiatry.spa'

    name= fields.Char(string=u'Sustancia psicoactiva', size=150, required=True)

class PsychiatryDrug(models.Model):
    _name = 'psychiatry.drug'

    name= fields.Char(string=u'Medicamento', size=150, required=True)

class PsychiatryDiseases(models.Model):
    _name = 'psychiatry.diseases'

    code_dx= fields.Char(string=u'Código', size=4, required=True)
    name= fields.Char(string=u'Diagnóstico', size=256, required=True)
    psychiatry= fields.Boolean('Dx Psiquiatría')
    vts= fields.Boolean('Dx Virus de Transmisión Sanguínea - VTS')
    others= fields.Boolean('Dx - Otros')

class PsychiatryHospitalization(models.Model):
    _name = "psychiatry.hospitalization"

    name = fields.Char(string=u'Número')
    date_in= fields.Date(string=u'Fecha de ingreso', default=fields.Date.today(), required=True)
    patient_id= fields.Many2one('res.partner', string=u'Paciente', required=True)
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
    category_id= fields.Many2many(related='patient_id.category_id', store=True, string='Etiqueta')
    sex = fields.Selection(related='patient_id.sex', store=True, string='Sexo')
    age = fields.Integer(compute='_age_ing', string="Edad", store=True)
    rango_edad= fields.Many2one('psychiatry.rango.edad', string='Rango de edad')
    day_stay = fields.Integer(compute='_day_stay', string="Días de estancia", store=True)
    hospitalization_count= fields.Integer(compute='_count_hospitalization', string=u'Ingresos')
    hospitalization_ids= fields.One2many('psychiatry.hospitalization','patient_id','Ingresos')
    state = fields.Selection(
            [('draft', 'Draft'),
             ('cancel', 'Cancelled'),
             ('abierto', 'Abierto'),
             ('egreso', 'Egreso'),
             ('finalizar', 'Finalizar')
            ], 'Status', readonly=True, track_visibility='onchange', copy=False, default='draft')

    #~ def button_confirm(self, cr, uid, ids, context=None):
        #~ return self.write(cr, uid, ids, {'state': 'confirm'}, context=context)
#~ 
    #~ def button_cancel(self, cr, uid, ids, context=None):
        #~ return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
#~ 
     #~ def button_egreso(self, cr, uid, ids, context=None):
        #~ return self.write(cr, uid, ids, {'state': 'egreso'}, context=context)
#~ 
    #~ def button_finalizar(self, cr, uid, ids, context=None):
        #~ return self.write(cr, uid, ids, {'state': 'finalizar'}, context=context)

    @api.multi
    def button_confirm(self):
        self.signal_workflow('confirm')
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def confirm(self):
        self.action_move_line_create()    
        
    @api.depends('patient_id.birth_date', 'date_in')
    def _age_ing(self):

        if self.patient_id.birth_date and self.date_in:
            d1 = datetime.strptime(self.patient_id.birth_date, "%Y-%m-%d").date()
            d2 = datetime.strptime(self.date_in, "%Y-%m-%d").date()
            self.age = relativedelta(d2, d1).years

    @api.depends('date_out', 'date_in')
    def _day_stay(self):

        if self.date_in and self.date_out:
            d1 = datetime.strptime(self.date_in, "%Y-%m-%d")
            d2 = datetime.strptime(self.date_out, "%Y-%m-%d")
            dur = (d2 - d1) 
            self.day_stay = dur.days +1
        logger.info('d1')
        logger.info(d1)
        logger.info('d2')
        logger.info(d2)
        
    @api.depends('hospitalization_ids')
    def _count_hospitalization(self):
        for record in self:
            record.hospitalization_count = len(record.hospitalization_ids)

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('hospitalization.sequence')
            })
        return super(PsychiatryHospitalization, self).create(vals)

    @api.onchange('age')
    def _onchange_rango_edad(self):
        rango_id = []
        for record in self:
            if record.age:
                rango_id = self.env['psychiatry.rango.edad'].search([('rango_inic','<=', record.age), ('rango_fin','>=', record.age)], limit=1)
                rango_id = rango_id.id
            logger.info('rangoedad')
            logger.info(rango_id)
        self.rango_edad = rango_id

class PsychiatrySpaConsume(models.Model):
    _name = "psychiatry.spa.consume"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    spa_id= fields.Many2one('psychiatry.spa', string=u'SPA', required=True)

class PsychiatryDrugsIn(models.Model):
    _name = "psychiatry.drugs.in"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    drug_id= fields.Many2one('psychiatry.drug', string=u'Medicamento', required=True)

class PsychiatryDrugsOut(models.Model):
    _name = "psychiatry.drugs.out"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    drug_id= fields.Many2one('psychiatry.drug', string=u'Medicamento', required=True)

class PsychiatryDiseasesPsychiatry(models.Model):
    _name = "psychiatry.diseases.psychiatry"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    diseases_id= fields.Many2one('psychiatry.diseases', string=u'Patología', required=True)
    diseases_type= fields.Selection([('1', 'Nuevo'), ('2', 'Antiguo')], string=u'Tipo', required=True)

class PsychiatryDiseasesOthers(models.Model):
    _name = "psychiatry.diseases.others"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    diseases_id= fields.Many2one('psychiatry.diseases', string=u'Patología', required=True)
    diseases_type= fields.Selection([('1', 'Nuevo'), ('2', 'Antiguo')], string=u'Tipo', required=True)

class PsychiatryEvolutions(models.Model):
    _name = "psychiatry.evolutions"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    date_evolution= fields.Date(default=fields.Date.today(), required=True)
    comment= fields.Char(string=u'Observaciones', required=True)

class PsychiatryReview(models.Model):
    _name = "psychiatry.review"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    date_review= fields.Date(default=fields.Date.today(), required=True)
    comment= fields.Char(string=u'Observaciones', required=True)

class PsychiatryLeaves(models.Model):
    _name = "psychiatry.leaves"

    hospitalization_id= fields.Many2one('psychiatry.hospitalization', ondelete='cascade')
    date_leave= fields.Date(default=fields.Date.today(), required=True)
    leave_type= fields.Selection([('1', 'Ninguno'), ('2', 'Día Completo'),
                                  ('3', 'Medio día'), ('4', 'Salida - Visita')],
                                  string=u'Tipo', required=True)
