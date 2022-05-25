# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class FhaSubventionExpense(models.Model):
    _name = "fha.subvention.expense"

    _inherit = ["mail.thread", "mail.activity.mixin"]

    _description = "Subvention Expense"

    item_id = fields.Many2one(
        comodel_name='fha.subvention.item',
        store=True,
        required=True,
        string='Item',
        track_visibility='always',
    )
    subvention_id = fields.Many2one(
        string="Subvention",
        related='item_id.subvention_id',
        store=True,
        readonly=True,
    )
    line_id = fields.Many2one(
        comodel_name='account.move.line',
        store=True,
        required=True,
        string='Account Line',
        track_visibility='always',
    )
    name = fields.Char(
        string='Name',
        help='Expense Description',
        required=True,
        index=True,
        track_visibility='always',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True,
    )
    date = fields.Date(
        required=True,
        string='Date',
        default=fields.Date.context_today,
        help='Expense Date',
    )
    total_expense = fields.Monetary(
        help='The total expense.',
        required=True,
        string='Total',
        currency_field='currency_id',
        track_visibility='always',
    )
    item_concept_name = fields.Char(
        'Subvention Concept',
        compute='_compute_complete_name',
        store=True
    )

    @api.depends('item_id')
    def _compute_complete_name(self):
        for expense in self:
            expense.item_concept_name = '%s %s - %s' % (
            expense.item_id.subvention_id.name, expense.item_id.subvention_id.code, expense.item_id.concept_id.name)
