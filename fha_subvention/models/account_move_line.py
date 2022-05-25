# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    subvention_id = fields.Many2one(
        'fha.subvention',
        string='Subvention',
    )
    item_id = fields.Many2one(
        'fha.subvention.item',
        string="Subvention Item",
    )
    expense_id = fields.Many2one(
        'fha.subvention.expense',
        'line_id',
        string='Account move lines',
    )

