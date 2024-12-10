from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_variety_id = fields.Many2one(
        comodel_name='product.variety',
        string='Product Variety'
    )

    product_variety_available_ids = fields.Many2many(
        comodel_name='product.variety',
        string='Product Varieties',
        related='product_id.categ_id.product_variety_ids',
        readonly=True
    )
