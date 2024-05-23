# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HolidaysRequest(models.Model):
    _inherit = "hr.leave"
    holiday_type_name = fields.Char(related="holiday_status_id.name", store=True)
    name = fields.Char('Time Off Type', required=True, translate=True)
    event_id = fields.Many2one('event.event', 'Evento', store=True, readonly=False)
    rol = fields.Selection([('oyente', 'Oyente'), ('speaker', 'Speaker'), ('moderador', 'Moderador')], string='Rol', required=True, default='oyente')
    project_id = fields.Many2one('project.project', 'Proyecto', store=True, readonly=False)
    grant_agreer = fields.Boolean(default=False, string="Mandatorio por Grant Agreer")
    cost = fields.Float("Coste", store=True)
    cost_type = fields.Selection(
        [
            ("own", "Own resources"),
            ("subsidized", "Subsidized"),
        ])
