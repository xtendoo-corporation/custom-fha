from odoo import _, api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    department_id = fields.Many2one(
        comodel_name="hr.department",
        required=True,
    )

    @api.depends('amount_total')
    def _compute_is_over_limit(self):
        for sale in self:
            sale.is_over_limit = sale.amount_total >= 12000

    is_over_limit = fields.Boolean(
        compute='_compute_is_over_limit',
    )
