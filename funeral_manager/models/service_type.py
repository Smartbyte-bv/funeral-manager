from odoo import fields, models, api, _


class ServiceType(models.Model):
    _name = 'service.type'
    _description = 'Service Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    def _default_domain_variant_1_ids(self):
        product_ids = self.env['product.product'].search([])
        filtered_product_ids = product_ids.filtered(lambda r: r.categ_id.variant_1)
        return [('id', 'in', filtered_product_ids.ids)]

    def _default_domain_variant_2_ids(self):
        product_ids = self.env['product.product'].search([])
        filtered_product_ids = product_ids.filtered(lambda r: r.categ_id.variant_2)
        return [('id', 'in', filtered_product_ids.ids)]

    def _default_domain_variant_3_ids(self):
        product_ids = self.env['product.product'].search([])
        filtered_product_ids = product_ids.filtered(lambda r: r.categ_id.variant_3)
        return [('id', 'in', filtered_product_ids.ids)]

    name = fields.Selection([('Bgrafenis', 'Begrafenis'), ('Plechtigheid aan de urne', 'Plechtigheid aan de urne'),
                             ('Kerkdienst aan de urne', 'Kerkdienst aan de urne'),
                             ('Plechtigheid aan de kist', 'Plechtigheid aan de kist'),
                             ('Enkel begraafplaats', 'Enkel begraafplaats')])

    notes = fields.Char()
    line_ids = fields.One2many('service.type.line', 'service_type_id')
    supplement_out_of_hours = fields.Selection([('no', 'No'), ('yes', 'Yes')], default='no',
                                               string="Supplement Saturday/out of hours")
    supplement_out_of_hours_price = fields.Float('Supplement Saturday/out of hours(Price)')
    product_product_1 = fields.Many2one('product.product', domain=lambda self: self._default_domain_variant_1_ids())
    product_product_2 = fields.Many2one('product.product', domain=lambda self: self._default_domain_variant_2_ids())
    product_product_3 = fields.Many2one('product.product', domain=lambda self: self._default_domain_variant_3_ids())


class ServiceTypeLine(models.Model):
    _name = 'service.type.line'
    _description = 'Service Type Line'

    product_id = fields.Many2one('product.product')
    description = fields.Char()
    qty = fields.Float()
    selling_price = fields.Float()
    service_type_id = fields.Many2one('service.type')
