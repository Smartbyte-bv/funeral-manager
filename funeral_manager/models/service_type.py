from odoo import fields, models, api, _


class ServiceType(models.Model):
    _name = 'service.type'
    _description = 'Service Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name')
    notes = fields.Char()
    line_ids = fields.One2many('service.type.line', 'service_type_id')
    aula_line_ids = fields.One2many('aula.line', 'service_type_id')
    print_works_line_ids = fields.One2many('print.works.line', 'service_type_id')
    transportation_line_ids = fields.One2many('transportation.line', 'service_type_id')
    coffee_table_line_ids = fields.One2many('coffee.table.line', 'service_type_id')
    other_cost_line_ids = fields.One2many('other.cost.line', 'service_type_id')
    contact_person_ids = fields.One2many('contact.person', 'service_type_id')
    flowers_ids = fields.One2many('flowers.line', 'service_type_id')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=["company_id"], store=True,
                                  ondelete="restrict")


class ServiceTypeLine(models.Model):
    _name = 'service.type.line'
    _description = 'Service Type Line'

    product_id = fields.Many2one('product.template')
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    service_type_id = fields.Many2one('service.type')
    taxes_id = fields.Many2many('account.tax', string="Tax")

    currency_id = fields.Many2one(related='service_type_id.currency_id', depends=['service_type_id.currency_id'],
                                  store=True,
                                  string='Currency')
    price_unit = fields.Float()
    price_subtotal = fields.Float(compute="_compute_amount", store=True, readonly=False)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.taxes_id = self.product_id.taxes_id.ids
        self.price_unit = self.product_id.list_price

    @api.depends('qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class AulaLine(models.Model):
    _name = 'aula.line'
    _description = 'Aula Line'

    product_id = fields.Many2one('product.template')
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    service_type_id = fields.Many2one('service.type')
    taxes_id = fields.Many2many('account.tax', string="Tax")
    currency_id = fields.Many2one(related='service_type_id.currency_id', depends=['service_type_id.currency_id'],
                                  store=True,
                                  string='Currency')
    price_unit = fields.Float()
    price_subtotal = fields.Float(compute="_compute_amount", store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.taxes_id = self.product_id.taxes_id.ids
        self.price_unit = self.product_id.list_price

    @api.depends('qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class PrintWorksLine(models.Model):
    _name = 'print.works.line'
    _description = 'Print Works Line'

    product_id = fields.Many2one('product.template')
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    service_type_id = fields.Many2one('service.type')
    taxes_id = fields.Many2many('account.tax', string="Tax")
    currency_id = fields.Many2one(related='service_type_id.currency_id', depends=['service_type_id.currency_id'],
                                  store=True,
                                  string='Currency')
    price_unit = fields.Float()
    price_subtotal = fields.Float(compute="_compute_amount", store=True, readonly=False)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.taxes_id = self.product_id.taxes_id.ids
        self.price_unit = self.product_id.list_price

    @api.depends('variant_id', 'product_id')
    def _get_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = (rec.price_unit + sum(rec.variant_id.mapped('variant_price')))

    @api.depends('qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class TransportationLine(models.Model):
    _name = 'transportation.line'
    _description = 'Transportation Line'

    product_id = fields.Many2one('product.template')
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    service_type_id = fields.Many2one('service.type')
    taxes_id = fields.Many2many('account.tax', string="Tax")
    currency_id = fields.Many2one(related='service_type_id.currency_id', depends=['service_type_id.currency_id'],
                                  store=True,
                                  string='Currency')
    price_unit = fields.Float()
    price_subtotal = fields.Float(compute="_compute_amount", store=True, readonly=False)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.taxes_id = self.product_id.taxes_id.ids
        self.price_unit = self.product_id.list_price

    @api.depends('qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class CoffeeTableLine(models.Model):
    _name = 'coffee.table.line'
    _description = 'Coffee Table Line'

    product_id = fields.Many2one('product.template')
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    service_type_id = fields.Many2one('service.type')
    taxes_id = fields.Many2many('account.tax', string="Tax")
    currency_id = fields.Many2one(related='service_type_id.currency_id', depends=['service_type_id.currency_id'],
                                  store=True,
                                  string='Currency')
    price_unit = fields.Float()
    price_subtotal = fields.Float(compute="_compute_amount", store=True, readonly=False)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.taxes_id = self.product_id.taxes_id.ids
        self.price_unit = self.product_id.list_price

    @api.depends('qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class OtherCostLine(models.Model):
    _name = 'other.cost.line'
    _description = 'Other Cost Line'

    product_id = fields.Many2one('product.template')
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    service_type_id = fields.Many2one('service.type')
    taxes_id = fields.Many2many('account.tax', string="Tax")
    currency_id = fields.Many2one(related='service_type_id.currency_id', depends=['service_type_id.currency_id'],
                                  store=True,
                                  string='Currency')
    price_unit = fields.Float()
    price_subtotal = fields.Float(compute="_compute_amount", store=True, readonly=False)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.taxes_id = self.product_id.taxes_id.ids
        self.price_unit = self.product_id.list_price

    @api.depends('qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class ContactPerson(models.Model):
    _name = 'contact.person'
    _description = 'Contact Person'

    partner_id = fields.Many2one('res.partner')
    email = fields.Char(related="partner_id.email", readonly=False)
    phone = fields.Char(related="partner_id.phone", readonly=False)
    city = fields.Char(related="partner_id.city", readonly=False)
    country_id = fields.Many2one(related="partner_id.country_id", readonly=False)
    relationship = fields.Char()
    signature = fields.Image('Signature', help='Signature', copy=False, attachment=True)
    service_type_id = fields.Many2one('service.type')


class FlowersLine(models.Model):
    _name = 'flowers.line'
    _description = 'Flowers Line'

    product_id = fields.Many2one('product.template')
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float(default=1)
    service_type_id = fields.Many2one('service.type')
    # is_invoice = fields.Boolean('Is Invoiced ?')
    taxes_id = fields.Many2many('account.tax', string="Tax")
    currency_id = fields.Many2one(related='service_type_id.currency_id', depends=['service_type_id.currency_id'],
                                  store=True,
                                  string='Currency')
    price_unit = fields.Float()
    price_subtotal = fields.Float(compute="_compute_amount", store=True, readonly=False)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    part_of_service = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    invoice_to = fields.Many2one('res.partner')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.taxes_id = self.product_id.taxes_id.ids
        self.price_unit = self.product_id.list_price

    @api.depends('qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
