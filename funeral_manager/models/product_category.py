from odoo import fields, models, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    variant_1 = fields.Boolean('Variant 1')
    variant_2 = fields.Boolean('Variant 2')
    variant_3 = fields.Boolean('Variant 3')


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    variant_price = fields.Float('')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    funeral_id = fields.Many2one('funeral.management')
