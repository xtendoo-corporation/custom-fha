# Copyright 2021 Xtendoo - Manuel Calero
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import Form, SavepointCase


class TestFhaSubvention(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.groups_id += cls.env.ref('analytic.group_analytic_accounting')
        cls.env.user.groups_id += cls.env.ref('analytic.group_analytic_tags')
        cls.env.user.groups_id += cls.env.ref('fha_subvention.group_fha_administrator_subvention')

    def _create_subvention(self):
        with Form(
            self.env["account.analytic.group"],
            view="analytic.account_analytic_group_form_view",
        ) as form:
            form.name = "Subvention test"
            form.description = "Subvention test description"
            form.partner_id = self.env.ref('base.res_partner_1')
            form.percentage = 70
            form.total_subvention = 1000
            with form.account_analytic_account_ids.new() as line:
                line.name = 'Foods'
                line.total_subvention = 100
                line.percentage = 50
        return form.save()

    def _create_bill(self):
        account_id = self.env['account.analytic.account'].search([('name', '=', 'Foods')], limit=1)
        with Form(self.env["account.move"].with_context(default_type="in_invoice")) as form:
            form.partner_id = self.env.ref('base.res_partner_1')
            with form.invoice_line_ids.new() as line:
                line.name = 'Foods with customer'
                line.analytic_account_id = account_id
                line.price_unit = 100.0
                line.quantity = 1
                line.tax_ids.clear()
        return form.save()

    def test_create_subvention(self):
        account_analytic = self._create_subvention()
        self.assertEqual(account_analytic.annual_subvention, 700)

    def test_create_bill(self):
        bill = self._create_bill()
        bill.post()
        self.assertEqual(bill.amount_total, 100)

    def test_assign_bill_to_subvention(self):
        account_analytic = self._create_subvention()
        bill = self._create_bill()
        bill.action_post()
        self.assertEqual(account_analytic.justified_subvention, 50)
