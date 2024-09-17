from odoo import _, api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    department_id = fields.Many2one(
        comodel_name="hr.department",
        required=True,
    )

    @api.depends('amount_total')
    def _compute_is_over_limit(self):
        for purchase in self:
            purchase.is_over_limit = purchase.amount_total >= 12000

    is_over_limit = fields.Boolean(
        compute='_compute_is_over_limit',
    )
    @api.onchange('amount_total')
    def _onchange_amount_total(self):
        self.is_over_limit = self.amount_total >= 12000

