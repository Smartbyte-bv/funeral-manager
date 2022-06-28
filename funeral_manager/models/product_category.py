from odoo import fields, models, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    variant_1 = fields.Boolean('Variant 1')
    variant_2 = fields.Boolean('Variant 2')
    variant_3 = fields.Boolean('Variant 3')
