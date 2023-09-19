# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    website = fields.Char(string="Sitio Web", store=True)
    organization_contact = fields.Char(string="Persona de contacto", store=True)

    assistence_number = fields.Integer(string="Número de asistentes")
    public_type = fields.Selection([('general', 'General'), ('profesional', 'Profesional'), ('cientifico', 'Científico')], string='Tipo de público', required=True, default='general')
    assistence_description = fields.Text(string="Descripcíon de la experiencia", store=True)

    image_ids = fields.One2many(
        'event.image',
        'event_id',
        string='Imágenes del Evento'
    )
