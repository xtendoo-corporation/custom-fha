from odoo import api, fields, models, Command, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    analytic_distribution = fields.Json(string='Analytic Distribution')
    analytic_precision = fields.Integer(
        store=False,
        default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),
    )

    @api.onchange('order_line')
    def _onchange_quick_edit_line_ids(self):
        for line in self.order_line:
            if not line.analytic_distribution:
                if hasattr(line, 'analytic_distribution'):
                    line.analytic_distribution = self.analytic_distribution
