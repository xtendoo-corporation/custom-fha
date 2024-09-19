{
    "name": "FHA DMS Employee",
    "category": "Employee",
    "version": "16.0.1.0",
    "author": "Xtendoo",
    "depends": [
        "hr",
        "dms",
        "dms_field",
        "hr_dms_field",
    ],
    "description": """
        Create DMS page  Employee.
        """,
    "data": [
        "views/hr_employee_form_view.xml",
        "views/dms_directory.xml",
    ],
    "installable": True,
    "auto_install": True,
}
