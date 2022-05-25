# -*- coding: utf-8 -*-
{
    'name': 'Subvention',
    "version": "13.0.1.0.0",
    'category': 'Tools',
    'summary': 'Centralize your subventions',
    'description': """
    This module offers the possibility of managing your subventions
""",
    'depends': ['base', 'mail'],
    'data': [
        'security/fha_subvention_security.xml',
        'security/ir.model.access.csv',
        'views/fha_subvention_view.xml',
        'views/fha_subvention_code_view.xml',
        'views/fha_subvention_concept_view.xml',
        'views/fha_subvention_expense_view.xml',
        'data/fha_subvention_data.xml',
    ],
    'application': True,
}
