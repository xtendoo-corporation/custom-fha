# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountAnalyticGroup(models.Model):
    _name = 'account.analytic.group'
    _inherit = ['account.analytic.group', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    is_readonly = fields.Boolean(
        string='Read Only',
        compute='_compute_readonly_subvention',
    )

    def _get_default_is_subvention(self):
        return self._context.get('in_subvention_app', False)

    subvention = fields.Boolean(
        string='Subvention Deprecated',
        default=False,
    )
    is_subvention = fields.Boolean(
        string='Is Subvention',
        default=_get_default_is_subvention,
    )
    code = fields.Char(
        string='Subvention Code',
        help='Code of subvention.',
        required=True,
        index=True,
        track_visibility='always',
        default=lambda self: self.env['ir.sequence'].next_by_code('fha.subvention'),
    )
    date_init = fields.Date(
        string='Init Date',
        required=True,
        track_visibility='always',
        default=lambda d: date(date.today().year, 1, 1),
    )
    date_end = fields.Date(
        string='End Date',
        required=True,
        track_visibility='always',
        default=lambda d: date(date.today().year, 12, 31),
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Entity',
        track_visibility='always',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True
    )
    total_subvention = fields.Monetary(
        string='Total Subvention',
        help='The total subvention.',
        currency_field='currency_id',
        track_visibility='always',
    )
    percentage = fields.Float(
        help='The percentage of subvention.',
        digits=(16, 2),
        track_visibility='always',
    )
    annual_subvention = fields.Monetary(
        string='Subsidized',
        help='The annual subvention.',
        currency_field='currency_id',
        track_visibility='always',
    )
    annual_spend = fields.Monetary(
        help='The annual spend.',
        currency_field='currency_id',
        track_visibility='always',
    )
    account_analytic_account_ids = fields.One2many(
        string='Subvention items',
        comodel_name='account.analytic.account',
        inverse_name='group_id',
        track_visibility='always',
    )
    justified_subvention = fields.Monetary(
        string='Justified Subvention',
        help='The justified subvention.',
        currency_field='currency_id',
        compute='_compute_justified_subvention',
    )
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        index=True,
        tracking=True,
        check_company=True,
        change_default=True,
    )

    def _compute_readonly_subvention(self):
        for record in self:
            record.is_readonly = not self.env.user.has_group('fha_subvention.group_fha_administrator_subvention')

    @api.depends('account_analytic_account_ids')
    def _compute_justified_subvention(self):
        for record in self:
            record.justified_subvention = sum(record.account_analytic_account_ids.mapped('total_expense'))

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if not self.env.user.has_group('fha_subvention.group_fha_administrator_subvention'):
            raise UserError(_('You have not permission to create Subventions'))
        return res

    @api.constrains('percentage')
    def _check_percentage(self):
        for record in self:
            if record.percentage < 1:
                raise ValidationError(_('The percentage of the subvention must be greater than one.'))
            if record.percentage > 100:
                raise ValidationError(_('The percentage of the subvention must be not over 100.'))

    @api.depends('name')
    def _compute_complete_name(self):
        for record in self:
            for line in record.account_analytic_account_ids:
                line._compute_complete_name()

    @api.onchange('percentage', 'total_subvention')
    def on_change_percentage(self):
        self.annual_subvention = self.total_subvention * self.percentage / 100
        self.annual_spend = self.total_subvention * self.percentage / 100

    def _get_default_project(self):
        project_id = self.env['project.project'].search([('name', '=', self.name )], limit=1)
        if project_id:
            return project_id
        project_id = self.env['project.project'].sudo().create({
            'name': self.name,
            'allow_timesheets': True,
        })
        return project_id

    def write(self, vals):
        if not vals.get('project_id'):
            vals['project_id'] = self._get_default_project()
        return super().write(vals)

