from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    product_variety_ids = fields.Many2many(
        comodel_name='product.variety',
        string='Product Varieties'
    )
