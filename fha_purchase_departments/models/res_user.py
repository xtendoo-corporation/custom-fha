from odoo import models, api, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    employee_id = fields.Many2one(string='Employee', comodel_name='hr.employee',)
