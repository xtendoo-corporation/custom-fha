# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountAnalyticDefault(models.Model):
    _name = "account.analytic.default"
    _description = "Analytic Distribution"
    _rec_name = "analytic_id"
    _order = "sequence"

    sequence = fields.Integer(string='Sequence', help="Gives the sequence order when displaying a list of analytic distribution")
    analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    product_id = fields.Many2one('product.product', string='Product', ondelete='cascade', help="Select a product which will use analytic account specified in analytic default (e.g. create new customer invoice or Sales order if we select this product, it will automatically take this as an analytic account)")
    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='cascade', help="Select a partner which will use analytic account specified in analytic default (e.g. create new customer invoice or Sales order if we select this partner, it will automatically take this as an analytic account)")
    account_id = fields.Many2one('account.account', string='Account', ondelete='cascade', help="Select an accounting account which will use analytic account specified in analytic default (e.g. create new customer invoice or Sales order if we select this account, it will automatically take this as an analytic account)")
    user_id = fields.Many2one('res.users', string='User', ondelete='cascade', help="Select a user which will use analytic account specified in analytic default.")
    company_id = fields.Many2one('res.company', string='Company', ondelete='cascade', help="Select a company which will use analytic account specified in analytic default (e.g. create new customer invoice or Sales order if we select this company, it will automatically take this as an analytic account)")
    date_start = fields.Date(string='Start Date', help="Default start date for this Analytic Account.")
    date_stop = fields.Date(string='End Date', help="Default end date for this Analytic Account.")

    @api.constrains('analytic_id', 'analytic_tag_ids')
    def _check_account_or_tags(self):
        if any(not default.analytic_id
               and not any(tag.analytic_distribution_ids for tag in default.analytic_tag_ids)
               for default in self
               ):
            raise ValidationError(_('An analytic default requires an analytic account or an analytic tag used for analytic distribution.'))

    @api.model
    def account_get(self, product_id=None, partner_id=None, account_id=None, user_id=None, date=None, company_id=None):
        domain = []
        if product_id:
            domain += ['|', ('product_id', '=', product_id)]
        domain += [('product_id', '=', False)]
        if partner_id:
            domain += ['|', ('partner_id', '=', partner_id)]
        domain += [('partner_id', '=', False)]
        if account_id:
            domain += ['|', ('account_id', '=', account_id)]
        domain += [('account_id', '=', False)]
        if company_id:
            domain += ['|', ('company_id', '=', company_id)]
        domain += [('company_id', '=', False)]
        if user_id:
            domain += ['|', ('user_id', '=', user_id)]
        domain += [('user_id', '=', False)]
        if date:
            domain += ['|', ('date_start', '<=', date), ('date_start', '=', False)]
            domain += ['|', ('date_stop', '>=', date), ('date_stop', '=', False)]
        best_index = -1
        res = self.env['account.analytic.default']
        for rec in self.search(domain):
            index = 0
            if rec.product_id: index += 1
            if rec.partner_id: index += 1
            if rec.account_id: index += 1
            if rec.company_id: index += 1
            if rec.user_id: index += 1
            if rec.date_start: index += 1
            if rec.date_stop: index += 1
            if index > best_index:
                res = rec
                best_index = index
        return res



class AccountAnalyticDistribution(models.Model):
    _name = 'account.analytic.distribution'
    _description = 'Analytic Account Distribution'
    _rec_name = 'account_id'

    account_id = fields.Many2one('account.analytic.account', string='Analytic Account', required=True)
    percentage = fields.Float(string='Percentage', required=True, default=100.0)
    name = fields.Char(string='Name', related='account_id.name', readonly=False)
    tag_id = fields.Many2one('account.analytic.tag', string="Parent tag", required=True)

    _sql_constraints = [
        ('check_percentage', 'CHECK(percentage >= 0 AND percentage <= 100)',
         'The percentage of an analytic distribution should be between 0 and 100.')
    ]

class AccountAnalyticTag(models.Model):
    _name = 'account.analytic.tag'
    _description = 'Analytic Tags'
    name = fields.Char(string='Analytic Tag', index=True, required=True)
    color = fields.Integer('Color Index')
    active = fields.Boolean(default=True, help="Set active to false to hide the Analytic Tag without removing it.")
    active_analytic_distribution = fields.Boolean('Analytic Distribution')
    analytic_distribution_ids = fields.One2many('account.analytic.distribution', 'tag_id', string="Analytic Accounts")
    company_id = fields.Many2one('res.company', string='Company')

class AccountAnalyticGroup(models.Model):
    _name = 'account.analytic.group'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _parent_store = True
    _rec_name = 'complete_name'

    name = fields.Char(
        required=True
    )
    description = fields.Text(
        string='Description'
    )
    parent_id = fields.Many2one(
        comodel_name='account.analytic.group',
        string="Parent",
        ondelete='cascade',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )
    parent_path = fields.Char(
        index=True
    )
    children_ids = fields.One2many(
        'account.analytic.group',
        'parent_id',
        string="Childrens"
    )
    complete_name = fields.Char(
        'Complete Name',
        compute='_compute_complete_name',
        recursive=True,
        store=True
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for group in self:
            if group.parent_id:
                group.complete_name = '%s / %s' % (group.parent_id.complete_name, group.name)
            else:
                group.complete_name = group.name

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )
    is_readonly = fields.Boolean(
        string='Read Only',
        compute='_compute_readonly_subvention',
    )

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result

    def _compute_readonly_subvention(self):
        for record in self:
            record.is_readonly = not self.env.user.has_group('fha_subvention.group_fha_administrator_subvention')

    subvention = fields.Boolean(
        string='Subvention Deprecated',
        default=False,
    )

    def _get_default_is_subvention(self):
        return self._context.get('in_subvention_app', False)

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

    @api.depends('account_analytic_account_ids')
    def _compute_justified_subvention(self):
        for record in self:
            record.justified_subvention = sum(record.account_analytic_account_ids.mapped('total_expense'))

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        index=True,
        tracking=True,
        check_company=True,
        change_default=True,
    )

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

