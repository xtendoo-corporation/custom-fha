# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "hr.leave"
    holiday_type_name = fields.Char(related="holiday_status_id.name")
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
    #event_website = fields.Char(string="Sitio Web", store=True)





    #Post Event
    # assistence_number = fields.Integer("Número de asistentes")
    # public_type = fields.Selection([('general', 'General'), ('profesional', 'Profesional'), ('cientifico', 'Científico')], string='Tipo de público', required=True, default='general')
    # assistence_description = fields.Char(string="Descripcíon", store=True)


    # applicant_name = fields.Char(string="Applicant name", store=True)
    #
    # event_type = fields.Char(string="Event type", store=True)
    # event_place = fields.Char(string="Event place", store=True)
    # event_date = fields.Date("Event date")
    # project_id = fields.Many2one('project.project', 'Project', store=True, readonly=False)
    # tittle = fields.Char(string="Tittle", store=True)
    # author = fields.Char(string="Author", store=True)
    # motivation = fields.Char(string="Motivation", store=True)
    # cost = fields.Float("Cost", store=True)
    # cost_type = fields.Selection(
    #     [
    #         ("own", "Own resources"),
    #         ("subsidized", "Subsidized"),
    #     ])
