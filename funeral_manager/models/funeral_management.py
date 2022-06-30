from odoo import fields, models, api, _


class FuneralManagement(models.Model):
    _name = 'funeral.management'
    _description = 'FuneralManagement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Request Number', required=True, copy=False,
        readonly=True, index=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner')
    phone = fields.Char(related="partner_id.phone", readonly=0)
    email = fields.Char(related="partner_id.email", readonly=0)
    dob = fields.Date(string="Date Of Birth")
    request_date = fields.Date('Request Date', default=fields.Datetime.now)
    responsible_service = fields.Many2one('res.users', tracking=True)
    service_type_id = fields.Many2one('service.type')
    funeral_service_line_id = fields.One2many('funeral.service.line', 'funeral_id')
    funeral_aula_ids = fields.One2many('funeral.aula', 'funeral_id')
    funeral_print_works_ids = fields.One2many('funeral.print.works', 'funeral_id')
    funeral_transportation_ids = fields.One2many('funeral.transportation', 'funeral_id')
    funeral_coffee_table_ids = fields.One2many('funeral.coffee.table', 'funeral_id')
    funeral_other_cost_ids = fields.One2many('funeral.other.cost', 'funeral_id')
    contact_person_ids = fields.One2many('funeral.contact.person', 'funeral_id')

    amount_untaxed = fields.Float(store=True, compute="get_total_price")
    amount_tax = fields.Float(store=True, compute="get_total_price")
    amount_total = fields.Float(store=True, compute="get_total_price")

    aula_amount_untaxed = fields.Float(store=True, compute="aula_get_total_price")
    aula_amount_tax = fields.Float(store=True, compute="aula_get_total_price")
    aula_amount_total = fields.Float(store=True, compute="aula_get_total_price")

    print_works_amount_untaxed = fields.Float(store=True, compute="print_works_get_total_price")
    print_works_amount_tax = fields.Float(store=True, compute="print_works_get_total_price")
    print_works_amount_total = fields.Float(store=True, compute="print_works_get_total_price")

    transportation_amount_untaxed = fields.Float(store=True, compute="transportation_get_total_price")
    transportation_amount_tax = fields.Float(store=True, compute="transportation_get_total_price")
    transportation_amount_total = fields.Float(store=True, compute="transportation_get_total_price")

    coffee_table_amount_untaxed = fields.Float(store=True, compute="coffee_table_get_total_price")
    coffee_table_amount_tax = fields.Float(store=True, compute="coffee_table_get_total_price")
    coffee_table_amount_total = fields.Float(store=True, compute="coffee_table_get_total_price")

    other_cost_amount_untaxed = fields.Float(store=True, compute="other_cost_get_total_price")
    other_cost_amount_tax = fields.Float(store=True, compute="other_cost_get_total_price")
    other_cost_amount_total = fields.Float(store=True, compute="other_cost_get_total_price")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=["company_id"], store=True,
                                  ondelete="restrict")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code('funeral.request') or _('New')
        return super(FuneralManagement, self).create(vals)

    @api.onchange('service_type_id')
    def _onchange_service_type(self):
        if self.funeral_service_line_id and self.service_type_id:
            self.contact_person_ids = False
            self.funeral_service_line_id.write({
                'funeral_id': False
            })
            self.funeral_aula_ids.write({
                'funeral_id': False
            })
            self.funeral_print_works_ids.write({
                'funeral_id': False
            })
            self.funeral_transportation_ids.write({
                'funeral_id': False
            })
            self.funeral_coffee_table_ids.write({
                'funeral_id': False
            })
            self.funeral_other_cost_ids.write({
                'funeral_id': False
            })
            # self.funeral_service_line_id.write({
            #     'product_variant_two': False
            # })
            # self.funeral_service_line_id.write({
            #     'product_variant_three': False
            # })
        lst = []
        for line in self.service_type_id.line_ids:
            lst.append(
                (0, 0, {
                    'description': line.description,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                    'taxes_id': line.taxes_id.ids,
                })
            )
        aula_lst = []
        for line in self.service_type_id.aula_line_ids:
            aula_lst.append(
                (0, 0, {
                    'description': line.description,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                    'taxes_id': line.taxes_id.ids,
                })
            )
        print_works_lst = []
        for line in self.service_type_id.print_works_line_ids:
            print_works_lst.append(
                (0, 0, {
                    'description': line.description,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                    'taxes_id': line.taxes_id.ids,
                })
            )
        transportation_lst = []
        for line in self.service_type_id.transportation_line_ids:
            transportation_lst.append(
                (0, 0, {
                    'description': line.description,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                    'taxes_id': line.taxes_id.ids,
                })
            )
        coffee_table_lst = []
        for line in self.service_type_id.coffee_table_line_ids:
            coffee_table_lst.append(
                (0, 0, {
                    'description': line.description,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                    'taxes_id': line.taxes_id.ids,
                })
            )
        other_cost_lst = []
        for line in self.service_type_id.other_cost_line_ids:
            other_cost_lst.append(
                (0, 0, {
                    'description': line.description,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                    'taxes_id': line.taxes_id.ids,
                })
            )
        self.write({
            'funeral_service_line_id': lst,
            'funeral_aula_ids': aula_lst,
            'funeral_print_works_ids': print_works_lst,
            'funeral_transportation_ids': transportation_lst,
            'funeral_coffee_table_ids': coffee_table_lst,
            'contact_person_ids': self.service_type_id.contact_person_ids,
            'funeral_other_cost_ids': other_cost_lst,
        })

    @api.depends('funeral_service_line_id')
    def get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_service_line_id:
                line_price = rec.funeral_service_line_id.mapped('price_subtotal')
                line_price_tax = rec.funeral_service_line_id.mapped('price_tax')
                price_tax = sum(line_price_tax)
                total = sum(line_price)
                # if rec.supplement_out_of_hours == "yes":
                #     total += rec.service_type_id.supplement_out_of_hours_price
                rec.amount_untaxed = total
                rec.amount_tax = price_tax
                rec.amount_total = rec.amount_untaxed + rec.amount_tax

    @api.depends('funeral_aula_ids')
    def aula_get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_aula_ids:
                line_price = rec.funeral_aula_ids.mapped(
                    'price_subtotal')
                line_price_tax = rec.funeral_aula_ids.mapped('price_tax')
                price_tax = sum(line_price_tax)
                total = sum(line_price)
                rec.aula_amount_untaxed = total
                rec.aula_amount_tax = price_tax
                rec.aula_amount_total = rec.aula_amount_untaxed + rec.aula_amount_tax

    @api.depends('funeral_print_works_ids')
    def print_works_get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_print_works_ids:
                line_price = rec.funeral_print_works_ids.mapped(
                    'price_subtotal')
                line_price_tax = rec.funeral_print_works_ids.mapped('price_tax')
                price_tax = sum(line_price_tax)
                total = sum(line_price)
                rec.print_works_amount_untaxed = total
                rec.print_works_amount_tax = price_tax
                rec.print_works_amount_total = rec.print_works_amount_untaxed + rec.print_works_amount_tax

    @api.depends('funeral_transportation_ids')
    def transportation_get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_transportation_ids:
                line_price = rec.funeral_transportation_ids.mapped(
                    'price_subtotal')
                line_price_tax = rec.funeral_transportation_ids.mapped('price_tax')
                price_tax = sum(line_price_tax)
                total = sum(line_price)
                rec.transportation_amount_untaxed = total
                rec.transportation_amount_tax = price_tax
                rec.transportation_amount_total = rec.transportation_amount_untaxed + rec.transportation_amount_tax

    @api.depends('funeral_coffee_table_ids')
    def coffee_table_get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_coffee_table_ids:
                line_price = rec.funeral_coffee_table_ids.mapped(
                    'price_subtotal')
                line_price_tax = rec.funeral_coffee_table_ids.mapped('price_tax')
                price_tax = sum(line_price_tax)
                total = sum(line_price)
                rec.coffee_table_amount_untaxed = total
                rec.coffee_table_amount_tax = price_tax
                rec.coffee_table_amount_total = rec.coffee_table_amount_untaxed + rec.coffee_table_amount_tax

    @api.depends('funeral_other_cost_ids')
    def other_cost_get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_other_cost_ids:
                line_price = rec.funeral_other_cost_ids.mapped(
                    'price_subtotal')
                line_price_tax = rec.funeral_other_cost_ids.mapped('price_tax')
                price_tax = sum(line_price_tax)
                total = sum(line_price)
                rec.other_cost_amount_untaxed = total
                rec.other_cost_amount_tax = price_tax
                rec.other_cost_amount_total = rec.other_cost_amount_untaxed + rec.other_cost_amount_tax


class FuneralServiceLine(models.Model):
    _name = 'funeral.service.line'
    _description = 'Funeral Service Line'

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    product_id = fields.Many2one('product.template')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float()
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
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

    @api.depends('qty', 'price_unit', 'taxes_id', 'variant_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit + sum(line.variant_id.mapped('variant_price'))
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class FuneralAula(models.Model):
    _name = 'funeral.aula'
    _description = 'Funeral Aula'

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    description = fields.Char(related="product_id.display_name", readonly=False)
    product_id = fields.Many2one('product.template')
    qty = fields.Float()
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
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

    @api.depends('qty', 'price_unit', 'taxes_id', 'variant_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit + sum(line.variant_id.mapped('variant_price'))
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class FuneralPrintWorks(models.Model):
    _name = 'funeral.print.works'
    _description = 'Funeral Print Works'

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    description = fields.Char(related="product_id.display_name", readonly=False)
    product_id = fields.Many2one('product.template')
    qty = fields.Float()
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
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

    @api.depends('qty', 'price_unit', 'taxes_id', 'variant_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit + sum(line.variant_id.mapped('variant_price'))
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class FuneralTransportation(models.Model):
    _name = 'funeral.transportation'
    _description = 'Funeral Transportation'

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    description = fields.Char(related="product_id.display_name", readonly=False)
    product_id = fields.Many2one('product.template')
    qty = fields.Float()
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
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

    @api.depends('qty', 'price_unit', 'taxes_id', 'variant_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit + sum(line.variant_id.mapped('variant_price'))
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class FuneralCoffeeTable(models.Model):
    _name = 'funeral.coffee.table'
    _description = 'Funeral Coffee Table'

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    description = fields.Char(related="product_id.display_name", readonly=False)
    product_id = fields.Many2one('product.template')
    qty = fields.Float()
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
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

    @api.depends('qty', 'price_unit', 'taxes_id', 'variant_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit + sum(line.variant_id.mapped('variant_price'))
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class FuneralOtherCost(models.Model):
    _name = 'funeral.other.cost'
    _description = 'Funeral Other Cost'

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    description = fields.Char(related="product_id.display_name", readonly=False)
    product_id = fields.Many2one('product.template')
    qty = fields.Float()
    product_template_attribute_lines = fields.One2many('product.template.attribute.line',
                                                       related="product_id.attribute_line_ids")
    value_ids = fields.Many2many('product.attribute.value', related="product_template_attribute_lines.value_ids")
    variant_id = fields.Many2many('product.attribute.value')
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

    @api.depends('qty', 'price_unit', 'taxes_id', 'variant_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit + sum(line.variant_id.mapped('variant_price'))
            taxes = line.taxes_id.compute_all(price, line.service_type_id.currency_id, line.qty,
                                              product=line.product_id, partner=False)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


class FuneralContactPerson(models.Model):
    _name = 'funeral.contact.person'
    _description = 'Funeral Contact Person'

    partner_id = fields.Many2one('res.partner')
    email = fields.Char(related="partner_id.email", readonly=False)
    phone = fields.Char(related="partner_id.phone", readonly=False)
    city = fields.Char(related="partner_id.city", readonly=False)
    country_id = fields.Many2one(related="partner_id.country_id", readonly=False)
    relationship = fields.Char()
    signature = fields.Image('Signature', help='Signature', copy=False, attachment=True)
    funeral_id = fields.Many2one('funeral.management')
