from odoo import api, fields, models, Command, _


class AccountMove(models.Model):
    _inherit = "account.move"

    analytic_distribution = fields.Json(string='Analytic Distribution')
    analytic_precision = fields.Integer(
        store=False,
        default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),
    )

    @api.onchange('invoice_line_ids')
    def _onchange_quick_edit_line_ids(self):
        res = super()._onchange_quick_edit_line_ids()
        for line in self.invoice_line_ids:
            if not line.analytic_distribution:
                if hasattr(line, 'analytic_distribution'):
                    line.analytic_distribution = self.analytic_distribution
        return res
