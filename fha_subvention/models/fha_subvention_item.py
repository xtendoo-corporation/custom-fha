# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class FhaSubventionItem(models.Model):
    _name = 'fha.subvention.item'

    _rec_name = 'concept_name'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = 'Subvention Item'

    subvention_id = fields.Many2one(
        comodel_name='fha.subvention',
        string='Subvention',
        track_visibility='always',
    )
    concept_id = fields.Many2one(
        comodel_name='fha.subvention.concept',
        store=True,
        required=True,
        string='Concept',
        track_visibility='always',
    )
    concept_name = fields.Char(
        related='concept_id.name',
        string='Name',
        readonly=True
    )
    expense_ids = fields.One2many(
        comodel_name='fha.subvention.expense',
        inverse_name='item_id',
        string='Expense',
        track_visibility='always',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True,
    )
    total_subvention = fields.Monetary(
        help='The total subvention concept.',
        currency_field='currency_id',
        track_visibility='always',
    )
    percentage = fields.Float(
        help='The percentage of subvention concept.',
        required=True,
        digits=(16, 2),
        track_visibility='always',
    )
    subvention_expense_ids = fields.One2many(
        comodel_name='fha.subvention.expense',
        inverse_name='item_id',
        string='Subvention items expenses',
    )
    total_expense = fields.Monetary(
        string='Total expense',
        compute='_compute_total_expense',
        currency_field='currency_id',
        help='Total expense in this item'
    )
    percentage_expense = fields.Float(
        string='Percentage expense',
        compute='_compute_percentage_expense',
        help='Percentage of expense in this item'
    )

    def _compute_total_expense(self):
        for record in self:
            record.total_expense = sum(record.subvention_expense_ids.mapped('total_expense'))

    def _compute_percentage_expense(self):
        for record in self:
            if record.total_subvention != 0:
                record.percentage_expense = record.total_expense / record.total_subvention * 100
            else:
                record.percentage_expense = 0

    def action_show_expenses(self):
        '''
        Open the expenses wizard
        '''
        self.ensure_one()
        # Get the view
        view = self.env.ref('fha_subvention.view_subvention_items_operations')
        return {
            'name': _('Expenses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fha.subvention.item',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'context': dict(
                self.env.context
            ),
        }
