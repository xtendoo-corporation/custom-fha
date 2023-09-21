# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from jinja2 import Template


class EventEvent(models.Model):
    _inherit = "event.event"

    website = fields.Char(string="Sitio Web", store=True)
    organization_contact = fields.Char(string="Persona de contacto", store=True)

    assistence_number = fields.Integer(string="Número de asistentes")
    public_type = fields.Selection([
        ('profesionales', 'Profesionales'),
        ('directivos', 'Directivos'),
        ('instituciones', 'Instituciones'),
        ('pymes_max_50', 'Pymes de hasta 50 trabajadores'),
        ('pymes_max_100', 'Pymes de hasta 100 trabajadores'),
        ('gran_empresa', 'Gran empresa'),
        ('comunidad_cientifica', 'Comunidad Científica'),
        ('sociedad_civil', 'Sociedad civil')], string='Tipo de público', required=True, default='profesionales')

    # public_type = fields.Selection([
    #     ('profesionales', 'Profesionales'),
    #     ('directivos', 'Directivos'),
    #     ('instituciones', 'Instituciones'),
    #     ('pymes_max_50', 'Pymes de hasta 50 trabajadores'),
    #     ('pymes_max_100', 'Pymes de hasta 100 trabajadores'),
    #     ('gran_empresa', 'Gran empresa'),
    #     ('comunidad_cientifica', 'Comunidad Científica'),
    #     ('sociedad_civil', 'Sociedad civil')
    # ], string='Tipo de público', required=True, default='profesionales')

    assistence_description = fields.Text(string="Descripcíon de la experiencia", store=True)

    image_ids = fields.One2many(
        'event.image',
        'event_id',
        string='Imágenes del Evento'
    )
    def button_done(self):
        self.write({'state': 'done'})
        self._onchange_state_event()


    @api.onchange('state')
    def _onchange_state_event(self):
       if self.state == 'done':
          self.send_email_with_template()

    # def send_email(self):
    #     self.ensure_one()
    #     template = self.env.ref('hr_leave_to_event.event_finish')
    #     email_message = template.send_mail(self.id, force_send=True)
    #     subject = email_message.subject or 'Evento Finalizado'
    #     message_body = f"Para: {self.user_id.name}\n\n{email_message.body}"
    #     self.message_post(
    #         body=message_body,
    #         message_type='comment',
    #         subtype_id=self.env.ref('mail.mt_comment').id,
    #         partner_ids=[(4, self.user_id.id)]
    #     )
    # def send_email(self):
    #     template = self.env.ref('hr_leave_to_event.event_finish')
    #     template_values = {
    #         'object': self,
    #         'object_name': self.name,
    #         'user_name': self.user_id.name
    #     }
    #     template_body = template.body_html
    #     rendered_template_body = Template(template_body).render(template_values)
    #     print("*"*120)
    #     print("template_values: ", template_values)
    #     print("rendered_template_body: ", rendered_template_body)
    #     print("*"*120)
    #
    #
    #     mail_obj = self.env['mail.mail']
    #     email_to = self.user_id.email
    #     subject = f"Evento {self.name} finalizado"
    #
    #     mail_id = mail_obj.create({
    #         'email_from': self.env.company.email,
    #         'email_to': email_to,
    #         'subject': subject,
    #         'body_html': Template(template_body).render(template_values),
    #     })
    #     mail_obj.send(mail_id)
    #     return True
    def send_email_with_template(self):
        # Supongamos que tienes una plantilla existente con un ID específico.
        template_id = self.env.ref('hr_leave_to_event.event_finish')

        # Compose the email using the template
        template = self.env['mail.template'].browse(template_id.id)
        template.send_mail(self.id, force_send=True)
