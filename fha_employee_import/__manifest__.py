{
    "name": "FHA Employee Import",
    "category": "Product",
    "version": "14.0.1.0",
    "author": "Xtendoo",
    "depends": [
        "hr_timesheet"
    ],
    "description": """
        Wizard to Import FHA Employee.
        """,
    "data": [
        "wizard/employee_timesheet_cost_import.xml",
        'security/ir.model.access.csv',
        "views/menu.xml",],
    "installable": True,
    "auto_install": True,
}
