# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"
    description = fields.Text(string="Descripcíon de la experiencia", store=True)
    website = fields.Char(string="Sitio Web", store=True)
    organizer = fields.Char(string="Organizador", store=True)
    address = fields.Char(string="Ubicación", store=True)
    organization_contact = fields.Char(string="Persona de contacto", store=True)
    rol = fields.Selection(
        [("oyente", "Oyente"), ("speaker", "Speaker"), ("moderador", "Moderador")],
        string="Rol",
        required=True,
        default="oyente",
    )
    name = fields.Char("Description")
    assistence_number = fields.Integer(string="Número de asistentes")
    public_type = fields.Selection(
        [
            ("profesionales", "Profesionales"),
            ("directivos", "Directivos"),
            ("instituciones", "Instituciones"),
            ("pymes_max_50", "Pymes de hasta 50 trabajadores"),
            ("pymes_max_100", "Pymes de hasta 100 trabajadores"),
            ("gran_empresa", "Gran empresa"),
            ("comunidad_cientifica", "Comunidad Científica"),
            ("sociedad_civil", "Sociedad civil"),
        ],
        string="Tipo de público",
        required=True,
        default="profesionales",
    )

    assistence_description = fields.Text(
        string="Descripcíon de la experiencia", store=True
    )

    image_ids = fields.One2many("event.image", "event_id", string="Imágenes del Evento")

    def compute_user_id_domain(self):
        domain = []
        if not self.env.user.has_group("event.group_event_manager"):
            domain = [("id", "=", self.env.user.id)]
        else:
            domain = []
        return domain

    user_id = fields.Many2one(
        "res.users",
        string="Responsible",
        default=lambda self: self.env.user,
        domain=lambda self: self.compute_user_id_domain(),
        tracking=True,
        readonly=False,
    )

    def button_done(self):
        self.write({"state": "done"})
        self._onchange_state_event()

    @api.onchange("state")
    def _onchange_state_event(self):
        if self.state == "done":
            self.send_email_with_template()
            self.send_email_comunication()

    def send_email_with_template(self):
        template_id = self.env.ref("hr_leave_to_event.event_finish")
        template = self.env["mail.template"].browse(template_id.id)
        template.send_mail(self.id, force_send=True)

    @api.model
    def get_communication_users(self):
        group = self.env["res.groups"].search([("name", "=", "Comunicación")])
        if group:
            users = self.env["res.users"].search([("groups_id", "in", group.ids)])
            return users
        else:
            return None

    def send_email_comunication(self):
        communication_users = self.get_communication_users()
        if communication_users:
            for user in communication_users:
                template_id = self.env.ref("hr_leave_to_event.event_pre_finish")
                template = self.env["mail.template"].browse(template_id.id)
                email_values = {
                    "email_to": user.email,
                }
                template.write(email_values)
                template.send_mail(self.id, force_send=True)

    @api.model
    def check_event_done(self):
        confirmed_events = self.search(
            [("state", "=", "confirm"), ("date_end", "<", fields.Datetime.now())]
        )
        for event in confirmed_events:
            event.button_done()
