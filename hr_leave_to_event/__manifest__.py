{
    'name': 'Ausencia por asistencia a evento',
    'summary': """Ausencia por asistencia a evento""",
    'version': '13.0.1.0.0',
    'description': """Ausencia por asistencia a evento""",
    'author': 'Dani Domínguez',
    'company': 'Xtendoo',
    'website': 'http://xtendoo.es',
    'category': 'Asistencias',
    'depends': [
        'hr_holidays',
        'project',
        'event',
    ],
    'license': 'AGPL-3',
    'data': [
        "views/hr_leave_views.xml",
        "views/event_event_views.xml",
        "data/hr_leave_type.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'auto_install': True,
}
