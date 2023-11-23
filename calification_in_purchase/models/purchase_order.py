# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from jinja2 import Template


class EventEvent(models.Model):
    _inherit = "purchase.order"

    calification = fields.Selection(
        [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
        "Calificación",
        default="0",
        tracking=True,
    )
