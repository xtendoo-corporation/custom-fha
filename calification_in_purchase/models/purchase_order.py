# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    calification = fields.Selection(
        [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
        "Calificación",
        default="0",
        tracking=True,
    )

BASE_EXCEPTION_FIELDS = ["message_follower_ids", "access_token", "calification"]


class TierValidation(models.AbstractModel):
    _inherit = "tier.validation"
    _description = "Tier Validation (abstract)"

    @api.model
    def _get_validation_exceptions(self, extra_domain=None, add_base_exceptions=True):
        """Return Tier Validation Exception field names that matchs custom domain."""
        exception_fields = (
            self.env["tier.validation.exception"]
            .sudo()
            .search(
                [
                    ("model_name", "=", self._name),
                    ("company_id", "in", [False] + self.env.company.ids),
                    "|",
                    ("group_ids", "in", self.env.user.groups_id.ids),
                    ("group_ids", "=", False),
                    *(extra_domain or []),
                ]
            )
            .mapped("field_ids.name")
        )
        if add_base_exceptions:
            exception_fields += BASE_EXCEPTION_FIELDS
        return list(set(exception_fields))
