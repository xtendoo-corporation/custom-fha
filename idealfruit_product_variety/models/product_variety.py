from odoo import models, fields

class ProductVariety(models.Model):
    _name = 'product.variety'
    _description = 'Product Variety'

    id = fields.Integer(string='ID', required=True)
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
