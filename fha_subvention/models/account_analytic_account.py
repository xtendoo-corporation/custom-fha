# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    _parent_name = 'group_id'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    def search(self, args=None, offset=0, limit=None, order=None, count=False):
        args = args or []
        if not args:
            return super(AccountAnalyticAccount, self).search(args, offset, limit, order, count)
        for condition in args:
            if condition[0] == 'name':
                condition[0] = 'complete_name'
        return super(AccountAnalyticAccount, self).search(args, offset, limit, order, count)

    def _get_default_is_subvention(self):
        return self._context.get('in_subvention_app', False)

    group_id = fields.Many2one(
        comodel_name='account.analytic.group',
        string='Group',
        check_company=True
    )
    subvention = fields.Boolean(
        string="Subvention Deprecated",
        default=False,
    )
    is_subvention = fields.Boolean(
        string="Is Subvention",
        default=_get_default_is_subvention,
    )
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True,
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
        default=0.0,
    )
    percentage = fields.Float(
        help='The percentage of subvention concept.',
        required=True,
        digits=(16, 2),
        track_visibility='always',
        default=1.0,
    )
    total_expense = fields.Monetary(
        string='Total expense',
        compute='_compute_total_expense',
        currency_field='currency_id',
        help='Total expense in this item',
    )
    percentage_expense = fields.Float(
        string='Percentage expense',
        compute='_compute_percentage_expense',
        help='Percentage of expense in this item',
    )
    account_analytic_line_ids = fields.One2many(
         comodel_name="account.analytic.line",
         inverse_name="account_id",
         string='Account analytic line',
         track_visibility="always",
    )
    account_analytic_account_ids = fields.One2many(
         comodel_name="account.analytic.account",
         inverse_name="group_id",
         string='Subvention items',
         track_visibility="always",
    )
    account_move_line_id = fields.One2many(
        comodel_name='account.move.line',
        inverse_name="analytic_account_id",
        string='Account Move Line',
    )

    def _get_name(self):
        return self.complete_name

    @api.depends('account_analytic_line_ids')
    def _compute_total_expense(self):
        for record in self:
            record.total_expense = sum(record.account_analytic_line_ids.mapped('justified_amount'))

    @api.constrains('percentage')
    def _check_percentage(self):
        for record in self:
            if record.percentage < 1:
                raise ValidationError(_("The percentage of the %s, must be greater than one.") % record.name)
            if record.percentage > 100:
                raise ValidationError(_("The percentage of the %s, must be not over 100.") % record.name)

    @api.onchange('total_subvention')
    def _compute_percentage_expense(self):
        self.percentage_expense = 0
        for record in self.filtered(lambda r: r.total_subvention != 0):
            record.percentage_expense = abs(record.total_expense) / record.total_subvention * 100

    @api.depends('name', 'group_id')
    def _compute_complete_name(self):
        for record in self:
            if record.group_id:
                record.complete_name = '%s / %s' % (record.group_id.name, record.name)
            else:
                record.complete_name = record.name

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("complete_name", operator, name), ("name", operator, name)]
        accounts = self.search(domain + args, limit=limit)
        return accounts.name_get()

    @api.depends('name')
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record.complete_name))
        return res

    def action_show_expenses(self):
        '''
        Open the expenses wizard
        '''
        self.ensure_one()
        # Get the view
        view = self.env.ref('fha_subvention.view_account_analytic_line')
        return {
            'name': _('Account Analytic Line'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.analytic.account',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'context': dict(self.env.context),
        }
