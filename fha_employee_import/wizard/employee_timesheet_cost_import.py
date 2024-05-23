# Copyright 2021 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging
from base64 import b64decode
from io import StringIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)

try:
    from csv import reader
except (ImportError, IOError) as err:
    _logger.error(err)


class EmployeeTimesheetCostImport(models.TransientModel):
    _name = "employee.timesheet.cost.import"
    _description = "Employee Timesheet Cost Import"

    data_file = fields.Binary(
        string="File to Import",
        required=True,
        help="Get you data file.",
    )
    filename = fields.Char()

    def import_file(self):
        """ Process the file chosen in the wizard. """
        self.ensure_one()
        data_file = b64decode(self.data_file)
        if not data_file:
            return
        self._parse_file(data_file)

    def update_employee(self, name, cost):
        if name == "":
            return _("Employee is empty")

        if cost == "":
            return _("Cost is empty in employee %s") % name

        cost = float(cost.replace(",", "."))
        if cost <= 0:
            return _("Time sheet must be positive")

        employee = self.env['hr.employee'].search([('name', 'ilike', name)], limit=1)
        if not employee:
            return _("Employee %s not found") % name

        employee.sudo().write(
                {
                    "timesheet_cost": cost,
                }
            )
        return False

    def parse_row(self, csv_data):
        error_list = []
        for row in csv_data:
            error = self.update_employee(row[0], row[1])
            if error:
                error_list.append(error)

        if error_list:
            raise UserError(
                _("Has errors, correct the errors and retry: " "\n%s") % "\n".join(error_list)
            )

    def _parse_file(self, data_file):
        try:
            data = StringIO(data_file.decode("utf-8"))
            csv_data = reader(data)
            next(csv_data)
        except Exception:
            raise UserError(_("Can not read the file"))
        self.parse_row(csv_data)
        return
