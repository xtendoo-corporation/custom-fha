# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class FhaSubventionTag(models.Model):
    _name = "fha.subvention.tag"

    _description = "Subvention Tag"

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

    name = fields.Char(
        string="Tag Name",
        required=True,
    )
    color = fields.Integer(
        string='Color Index',
    )
