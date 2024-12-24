# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"



    analytic_line_ids = fields.One2many('account.analytic.line', 'move_id', string='Analytic lines')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          index=True, compute="_compute_analytic_account_id", store=True,
                                          readonly=False, check_company=True, copy=True)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags',
                                        compute="_compute_analytic_tag_ids", store=True, readonly=False,
                                        check_company=True, copy=True)

    exclude_from_invoice_tab = fields.Boolean(
        help="Technical field used to exclude some lines from the invoice_line_ids tab in the form view.")

    @api.depends('product_id', 'account_id', 'partner_id', 'date')
    def _compute_analytic_tag_ids(self):
        for record in self:
            if not record.exclude_from_invoice_tab or not record.move_id.is_invoice(include_receipts=True):
                rec = self.env['account.analytic.default'].account_get(
                    product_id=record.product_id.id,
                    partner_id=record.partner_id.commercial_partner_id.id or record.move_id.partner_id.commercial_partner_id.id,
                    account_id=record.account_id.id,
                    user_id=record.env.uid,
                    date=record.date,
                    company_id=record.move_id.company_id.id
                )
                if rec:
                    record.analytic_tag_ids = rec.analytic_tag_ids

    def create_analytic_lines(self):
        context = self.env.context.copy()
        print("*" * 50)
        print("ENTRA EN CREATE ANALYTIC LINES")
        print("context",context)
        print("*" * 50)
        context.update({'in_subvention_app': True})
        self.env.context = context
        return super().create_analytic_lines()

    @api.depends('product_id', 'account_id', 'partner_id', 'date')
    def _compute_analytic_account_id(self):
        for record in self:
            if not record.exclude_from_invoice_tab or not record.move_id.is_invoice(include_receipts=True):
                rec = self.env['account.analytic.default'].account_get(
                    product_id=record.product_id.id,
                    partner_id=record.partner_id.commercial_partner_id.id or record.move_id.partner_id.commercial_partner_id.id,
                    account_id=record.account_id.id,
                    user_id=record.env.uid,
                    date=record.date,
                    company_id=record.move_id.company_id.id
                )
                if rec:
                    record.analytic_account_id = rec.analytic_id

