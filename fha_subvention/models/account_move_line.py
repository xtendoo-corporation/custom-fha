# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def create_analytic_lines(self):
        context = self.env.context.copy()
        context.update({'in_subvention_app': True})
        self.env.context = context
        return super().create_analytic_lines()
