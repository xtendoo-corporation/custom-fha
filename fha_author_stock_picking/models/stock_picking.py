# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        if not vals.get("user_id"):
            vals["user_id"] = self.env['sale.order'].search([('name', '=', vals.get("origin"))]).user_id.id
        return super().create(vals)
