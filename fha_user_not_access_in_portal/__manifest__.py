{
    'name': 'FHA user not access in portal',
    'summary': """FHA user not access in portal""",
    'version': '15.0.1.0.0',
    'description': """FHA user not access in portal""",
    'author': 'Dani Domínguez',
    'company': 'Xtendoo',
    'website': 'http://xtendoo.es',
    'category': 'Admin Tools',
    'depends': [
        'base',
        'sale',
        'dms',
        'portal',
        'hr_timesheet'
    ],
    'license': 'AGPL-3',
    'data': [
        # 'security/security_group.xml',
        'views/timesheet_portal_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
