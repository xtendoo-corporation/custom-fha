# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "hr.leave"
    holiday_type_name = fields.Char(related="holiday_status_id.name")
    name = fields.Char('Time Off Type', required=True, translate=True)

    applicant_name = fields.Char(string="Applicant name", store=True)
    event_id = fields.Many2one('event.event', 'Event name', store=True, readonly=False)
    event_type = fields.Char(string="Event type", store=True)
    event_place = fields.Char(string="Event place", store=True)
    event_date = fields.Date("Event date")
    project_id = fields.Many2one('project.project', 'Project', store=True, readonly=False)
    tittle = fields.Char(string="Tittle", store=True)
    author = fields.Char(string="Author", store=True)
    motivation = fields.Char(string="Motivation", store=True)
    cost = fields.Float("Cost", store=True)
    cost_type = fields.Selection(
        [
            ("own", "Own resources"),
            ("subsidized", "Subsidized"),
        ])
