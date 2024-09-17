# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class LeaveReportCalendar(models.Model):
    _inherit = "hr.leave.report.calendar"

    leave_name = fields.Char(string="Name", readonly=True)
    # start_datetime = fields.Datetime(string='From', readonly=True)
    # stop_datetime = fields.Datetime(string='To', readonly=True)
    # tz = fields.Selection(_tz_get, string="Timezone", readonly=True)
    # duration = fields.Float(string='Duration', readonly=True)
    # employee_id = fields.Many2one('hr.employee', readonly=True)
    # company_id = fields.Many2one('res.company', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, "hr_leave_report_calendar")

        self._cr.execute(
            """CREATE OR REPLACE VIEW hr_leave_report_calendar AS
        (SELECT
            row_number() OVER() AS id,
            ce.name AS name,
            ce.start_date AS start_datetime,
            ce.stop_date AS stop_datetime,
            ce.duration AS duration,
            hl.employee_id AS employee_id,
            em.company_id AS company_id,
            hl.holiday_type_name AS leave_name
        FROM hr_leave hl
            LEFT JOIN calendar_event ce
                ON ce.id = hl.meeting_id
            LEFT JOIN hr_employee em
                ON em.id = hl.employee_id
        WHERE
            hl.state = 'validate');
        """
        )
