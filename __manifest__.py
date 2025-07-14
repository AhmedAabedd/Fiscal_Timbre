# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Timbre Fiscal',
    'version' : '1.0',
    'summary': 'Timbre Fiscal',
    'sequence': 10,
    'description': '"Adding Timbre Fiscal"',
    'category': 'Productivity',
    'website': 'https://www.proosoftcloud.com/',
    'depends' : ['account'],
    'data': ['data/product_data.xml',
             'views/inherit_invoice_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}