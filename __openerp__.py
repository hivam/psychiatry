# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Psychiatry',
    'version' : '1.0',
    'summary': 'Psychiatric evaluation',
    'description': """
=================================================================
""",
    'category' : 'Health',
    'author' : 'Hector Ivan Valencia Muñoz',
    'website': 'http://www.odoo-co.blogspot.com',
    'license': 'AGPL-3',
    'depends' : [],
    'data' : [
                'security/psychiatry_security.xml',
                'security/ir.model.access.csv',
                'views/psychiatry_view.xml',
                'data/psychiatry_sequences.xml',
                #'data/psychiatry.diseases.csv',
                'data/psychiatry.answer.csv',
                'data/psychiatry.whoqolbref.question.csv',
                'data/psychiatry.scl90r.question.csv',
                'data/psychiatry.moca.question.csv',
                'data/psychiatry.sf36.question.csv',
                'data/psychiatry.spa.csv',
                'data/psychiatry.drug.csv'
              ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
