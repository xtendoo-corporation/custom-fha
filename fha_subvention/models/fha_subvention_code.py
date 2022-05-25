# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime, timedelta

from odoo import api, fields, models

class FhaSubventionTag(models.Model):
    _name = "fha.subvention.code"

    _description = "Subvention Code"

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Code name already exists !"),
    ]

    name = fields.Char(
        string="Code Name",
        required=True,
    )
    color = fields.Integer(
        string='Color Index',
    )

#
# Deprecated
#
# class FhaSubventionCode(models.Model):
#     _name = "fha.subvention.code"
#     _inherit = ["mail.thread", "mail.activity.mixin"]
#
#     _description = "Subvention Code"
#
#     _sql_constraints = [("unique_code", "UNIQUE(code)", "Code must be unique")]
#
#     name = fields.Char(
#         string="Name",
#         help="Name of subvention code.",
#         required=True,
#         index=True,
#         track_visibility="always",
#     )
#     code = fields.Char(
#         string="Code",
#         required=True,
#         copy=False,
#         track_visibility="always",
#     )
