# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FhaSubventionConcept(models.Model):
    _name = "fha.subvention.concept"

    _inherit = ["mail.thread", "mail.activity.mixin"]

    _description = "Subvention Concept"

    name = fields.Char(
        string="Name",
        help="Name of subvention concept.",
        required=True,
        index=True,
        track_visibility="always",
    )
    code_ids = fields.Many2many(
        string="Code",
        comodel_name='fha.subvention.code',
        required=True,
    )

    @api.constrains('code_ids')
    def _check_tags(self):
        for record in self:
            if len(record.code_ids) > 1:
                raise ValidationError(_("Error! more than one code is not allowed"))
