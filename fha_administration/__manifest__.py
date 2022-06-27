{
    'name': 'FHA Administration',
    'summary': """Administration settings for FHA""",
    'version': '13.0.1.0.0',
    'description': """Administration settings for FHA""",
    'author': 'Dani Domínguez',
    'company': 'Xtendoo',
    'website': 'http://xtendoo.es',
    'category': 'Admin Tools',
    'depends': [
        'base',
        'sale',
    ],
    'license': 'AGPL-3',
    'data': [
        'security/security_group.xml',
    ],
    'installable': True,
    'auto_install': True,
}
