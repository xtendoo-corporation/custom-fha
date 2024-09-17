# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    calification = fields.Selection(
        [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
        "Calificación",
        default="0",
        tracking=True,
        compute="_compute_calification",
    )

    def _compute_calification(self):
        for partner in self:
            purchase_orders = self.env["purchase.order"].search(
                [
                    ("partner_id", "=", partner.id),
                    ("state", "not in", ("draft", "cancel")),
                ]
            )
            if not purchase_orders:
                partner.calification_number = 0
                partner.show_calification = False
                partner.calification = "0"
            else:
                calification = 0
                for purchase_order in purchase_orders:
                    calification += int(purchase_order.calification)
                partner.calification_number = calification / len(purchase_orders)
                partner.show_calification = True
                partner.calification = str(int(round(partner.calification_number, 0)))

    calification_number = fields.Float("Calificación", compute="_compute_calification")
    show_calification = fields.Boolean(
        "Mostrar calificación", compute="_compute_calification"
    )
