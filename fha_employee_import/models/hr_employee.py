# Copyright 2021 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    timesheet_cost = fields.Monetary(
        'Timesheet Cost',
        currency_field='currency_id',
        groups="hr.group_hr_user",
        default=0.0,
        tracking=True,
    )
