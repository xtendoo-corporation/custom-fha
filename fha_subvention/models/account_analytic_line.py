# Copyright 2021 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    move_move_id = fields.Many2one(
        related='move_id.move_id',
        string='Invoice Number',
        readonly=True,
    )
    abs_amount = fields.Monetary(
        string='Absolute Amount',
        compute='_compute_amount',
        store=True,
    )
    subvention = fields.Boolean(
        string="Subvention Deprecated",
        default=False,
    )
    is_subvention = fields.Boolean(
        string='Is Subvention',
        related='group_id.subvention',
    )
    account_id = fields.Many2one(
        'account.analytic.account',
        'Subvention',
        required=False,
        ondelete='restrict',
        index=True,
        domain="[('is_subvention', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    justified_percentage = fields.Float(
        related='account_id.percentage',
        digits=(16, 2),
        default=0.0,
    )
    justified_amount = fields.Monetary(
        string='Justified Amount',
        help='The justified amount.',
        currency_field='currency_id',
        store=True,
        compute='_compute_justified_amount',
    )

    @api.depends('amount')
    def _compute_amount(self):
        for record in self:
            record.abs_amount = abs(record.amount)

    @api.depends('amount', 'justified_percentage')
    def _compute_justified_amount(self):
        self.justified_amount = 0
        for record in self.filtered(lambda r: r.amount != 0):
            record.justified_amount = abs(record.amount) * record.justified_percentage / 100
