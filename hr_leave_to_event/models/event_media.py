from odoo import api, fields, models


class EventImage(models.Model):
    _name = "event.image"
    _description = "Event Images"

    name = fields.Char("Nombre", required=True)
    sequence = fields.Integer(default=10, index=True)

    image_1920 = fields.Image(required=True, string="Imagen")

    event_id = fields.Many2one("event.event", "Evento", index=True, ondelete="cascade")

    @api.model
    def create(self, vals):
        if "event_id" not in vals:
            # Obtén el evento actual del contexto si está disponible
            event_id = self._context.get("default_event_id", False)
            if event_id:
                vals["event_id"] = event_id
        return super(EventImage, self).create(vals)
