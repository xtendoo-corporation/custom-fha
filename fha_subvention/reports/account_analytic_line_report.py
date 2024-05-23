# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountAnalyticLineView(models.TransientModel):
    _name = "account.analytic.line.view"
    _description = "Subvention View"
    _order = "account_id, employee_id, move_id.partner_id, date"

    date = fields.Datetime()
    name = fields.Char()
    amount = fields.Float()
    justified_amount = fields.Float()
    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
    )
    move_id = fields.Many2one(
        comodel_name='account.move.line',
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
    )

class AccountAnalyticLineReport(models.TransientModel):
    _name = "account.analytic.line.report"
    _description = "Subvention Report"

    date_from = fields.Date()
    date_to = fields.Date()
    analytic_group_id = fields.Many2one(
        comodel_name='account.analytic.group',
    )
    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
    )
    # Data fields, used to browse report data
    results = fields.Many2many(
        comodel_name="account.analytic.line.view",
        compute="_compute_results",
        help="Use compute fields, so there is nothing store in database",
    )

    def _compute_results(self):
        self.ensure_one()
        ReportLine = self.env["account.analytic.line.view"]
        date_from = self.date_from or "0001-01-01"
        date_to = self.date_to or fields.Date.context_today(self)
        account_ids = self.analytic_group_id.account_analytic_account_ids.ids

        print(":"*80)
        print("date_from :", date_from)
        print("date_to :", date_to)
        print("account_ids :", account_ids)
        print(":"*80)

        print("#"*80)
        print(
            """
            SELECT
                line.name,
                line.date,
                ABS(line.amount) AS amount,
                line.justified_amount,
                line.account_id,
                line.employee_id,
                line.move_id,
                partner.id AS partner_id
            FROM
                account_analytic_line line
                LEFT JOIN account_move_line account_move_line ON account_move_line.id = line.move_id
                LEFT JOIN account_move account_move ON account_move.id = account_move_line.move_id
                LEFT JOIN res_partner partner ON partner.id = account_move.partner_id
            WHERE
                CAST(line.date AS date) >= %s
                and
                CAST(line.date AS date) <= %s
                and
                line.account_id in %s
            ORDER BY line.account_id, line.employee_id, partner_id, line.date
        """,
            (
                date_from,
                date_to,
                tuple(account_ids)
            ),
        )
        print("#"*80)

        self._cr.execute(
            """
            SELECT
                line.name,
                line.date,
                ABS(line.amount) AS amount,
                line.justified_amount,
                line.account_id,
                line.employee_id,
                line.move_id,
                partner.id AS partner_id
            FROM
                account_analytic_line line
                LEFT JOIN account_move_line account_move_line ON account_move_line.id = line.move_id
                LEFT JOIN account_move account_move ON account_move.id = account_move_line.move_id
                LEFT JOIN res_partner partner ON partner.id = account_move.partner_id
            WHERE
                CAST(line.date AS date) >= %s
                and
                CAST(line.date AS date) <= %s
                and
                line.account_id in %s
            ORDER BY line.account_id, line.employee_id, partner_id, line.date
        """,
            (
                date_from,
                date_to,
                tuple(account_ids)
            ),
        )
        results = self._cr.dictfetchall()

        print(":"*80)
        for result in results:
            print("Result :", result)
        print(":"*80)

        self.results = [ReportLine.new(line).id for line in results]

    def print_report(self):
        self.ensure_one()
        action = self.env.ref("fha_subvention.action_account_analytic_line_report_pdf")
        return action.report_action(self, config=False)

    def _get_html(self):
        result = {}
        rcontext = {}
        report = self.browse(self._context.get("active_id"))
        if report:
            rcontext["o"] = report
            result["html"] = self.env.ref(
                "fha_subvention.action_account_analytic_line_report_html"
            ).render(rcontext)
        return result

    @api.model
    def get_html(self, given_context=None):
        return self.with_context(given_context)._get_html()
