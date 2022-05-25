# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class FhaSubvention(models.Model):
    _name = "fha.subvention"

    _inherit = ["mail.thread", "mail.activity.mixin"]

    _description = "Subvention"

    _sql_constraints = [("unique_code", "UNIQUE(code)", "Code must be unique")]

    name = fields.Char(
        string="Subvention Name",
        help="Name of subvention.",
        required=True,
        index=True,
        track_visibility="always",
    )
    code = fields.Char(
        string="Subvention Code",
        help="Code of subvention.",
        required=True,
        index=True,
        track_visibility="always",
        default=lambda self: self.env['ir.sequence'].next_by_code('fha.subvention'),
    )
    date_init = fields.Date(
        string="Init Date",
        required=True,
        track_visibility="always"
    )
    date_end = fields.Date(
        string="End Date",
        required=True,
        track_visibility="always",
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Entity',
        track_visibility="always",
    )
    description = fields.Text(
        String="Subvention Description",
        help="Description of subvention.",
        track_visibility="always"
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True
    )
    total_subvention = fields.Monetary(
        help="The total subvention.",
        currency_field='currency_id',
        track_visibility="always",
    )
    percentage = fields.Float(
        help="The percentage of subvention.",
        digits=(16, 2),
        track_visibility="always",
    )
    annual_subvention = fields.Monetary(
        help="The annual subvention.",
        currency_field='currency_id',
        track_visibility="always",
    )
    annual_spend = fields.Monetary(
        help="The annual spend.",
        currency_field='currency_id',
        track_visibility="always",
    )
    subvention_item_ids = fields.One2many(
        comodel_name="fha.subvention.item",
        inverse_name="subvention_id",
        string='Subvention items',
        track_visibility="always",
    )

    @api.onchange('percentage')
    def on_change_percentage(self):
        self.annual_subvention = self.total_subvention * self.percentage / 100
        self.annual_spend = self.total_subvention * self.percentage / 100

