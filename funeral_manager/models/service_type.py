from odoo import fields, models, api, _


class ServiceType(models.Model):
    _name = 'service.type'
    _description = 'Service Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Selection([('Bgrafenis', 'Begrafenis'), ('Plechtigheid aan de urne', 'Plechtigheid aan de urne'),
                             ('Kerkdienst aan de urne', 'Kerkdienst aan de urne'),
                             ('Plechtigheid aan de kist', 'Plechtigheid aan de kist'),
                             ('Enkel begraafplaats', 'Enkel begraafplaats')])

    notes = fields.Char()
    line_ids = fields.One2many('service.type.line', 'service_type_id')
    aula_line_ids = fields.One2many('aula.line', 'service_type_id')
    supplement_out_of_hours = fields.Selection([('no', 'No'), ('yes', 'Yes')], default='no',
                                               string="Supplement Saturday/out of hours")
    supplement_out_of_hours_price = fields.Float('Supplement Saturday/out of hours(Price)')


class ServiceTypeLine(models.Model):
    _name = 'service.type.line'
    _description = 'Service Type Line'

    product_id = fields.Many2one('product.template')
    variant_id = fields.Many2one('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    depend_selling_price = fields.Float(related="product_id.list_price")
    selling_price = fields.Float(compute="_get_selling_price", store=True)
    service_type_id = fields.Many2one('service.type')

    @api.depends('variant_id', 'product_id')
    def _get_selling_price(self):
        for rec in self:
            rec.selling_price = (rec.depend_selling_price + rec.variant_id.variant_price)

class AulaLine(models.Model):
    _name = 'aula.line'
    _description = 'Aula Line'

    product_id = fields.Many2one('product.template')
    variant_id = fields.Many2one('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    depend_selling_price = fields.Float(related="product_id.list_price")
    selling_price = fields.Float(compute="_get_selling_price", store=True)
    service_type_id = fields.Many2one('service.type')

    @api.depends('variant_id', 'product_id')
    def _get_selling_price(self):
        for rec in self:
            rec.selling_price = (rec.depend_selling_price + rec.variant_id.variant_price)
