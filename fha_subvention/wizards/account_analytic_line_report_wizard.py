# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import time

from odoo import models, fields
from odoo.tools.safe_eval import safe_eval


class AccountAnalyticLineReportWizard(models.TransientModel):
    _name = "account.analytic.line.report.wizard"
    _description = "Account Analytic Line Report Wizard"

    date_from = fields.Date(
        "Start Date",
        required=True,
        default=time.strftime('%Y-01-01'),
    )
    date_to = fields.Date(
        "End Date",
        required=True,
        default=fields.Date.context_today,
    )
    analytic_group_id = fields.Many2one(
        comodel_name='account.analytic.group',
        required=True,
        string='Subvention',
        domain="[('is_subvention', '=', True)]"
    )

    def button_export_html(self):
        self.ensure_one()
        action = self.env.ref("fha_subvention.action_account_analytic_line_report_html")
        vals = action.read()[0]
        context = vals.get("context", {})
        if context:
            context = safe_eval(context)
        model = self.env["account.analytic.line.report"]
        report = model.create(self._prepare_report())
        context["active_id"] = report.id
        context["active_ids"] = report.ids
        vals["context"] = context
        return vals

    def button_export_pdf(self):
        self.ensure_one()
        return self._export()

    def _prepare_report(self):
        self.ensure_one()
        return {
            "date_from": self.date_from,
            "date_to": self.date_to or fields.Date.context_today(self),
            "analytic_group_id": self.analytic_group_id.id,
        }

    def _export(self):
        model = self.env["account.analytic.line.report"]
        report = model.create(self._prepare_report())
        return report.print_report()
