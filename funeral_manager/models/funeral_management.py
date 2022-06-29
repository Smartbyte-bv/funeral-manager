from odoo import fields, models, api, _


class FuneralManagement(models.Model):
    _name = 'funeral.management'
    _description = 'FuneralManagement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    # def _default_domain_variant_1_ids(self):
    #     product_ids = self.env['product.product'].search([])
    #     filtered_product_ids = product_ids.filtered(lambda r: r.categ_id.variant_1)
    #     return [('id', 'in', filtered_product_ids.ids)]
    #
    # def _default_domain_variant_2_ids(self):
    #     product_ids = self.env['product.product'].search([])
    #     filtered_product_ids = product_ids.filtered(lambda r: r.categ_id.variant_2)
    #     return [('id', 'in', filtered_product_ids.ids)]
    #
    # def _default_domain_variant_3_ids(self):
    #     product_ids = self.env['product.product'].search([])
    #     filtered_product_ids = product_ids.filtered(lambda r: r.categ_id.variant_3)
    #     return [('id', 'in', filtered_product_ids.ids)]

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
    # supplement_out_of_hours = fields.Selection([('no', 'No'), ('yes', 'Yes')],
    #                                            string="Supplement Saturday/out of hours", default="no",
    #                                            related="service_type_id.supplement_out_of_hours", readonly=False)

    amount_untaxed = fields.Float(store=True, compute="get_total_price")
    amount_tax = fields.Float(store=True, compute="get_total_price")
    amount_total = fields.Float(store=True, compute="get_total_price")

    aula_amount_untaxed = fields.Float(store=True, compute="aula_get_total_price")
    aula_amount_tax = fields.Float(store=True, compute="aula_get_total_price")
    aula_amount_total = fields.Float(store=True, compute="aula_get_total_price")

    print_works_amount_untaxed = fields.Float(store=True, compute="aula_get_total_price")
    print_works_amount_tax = fields.Float(store=True, compute="aula_get_total_price")
    print_works_amount_total = fields.Float(store=True, compute="aula_get_total_price")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code('funeral.request') or _('New')
        return super(FuneralManagement, self).create(vals)

    @api.onchange('service_type_id')
    def _onchange_service_type(self):
        if self.funeral_service_line_id and self.service_type_id:
            self.funeral_service_line_id.write({
                'funeral_id': False
            })
            self.funeral_aula_ids.write({
                'funeral_id': False
            })
            self.funeral_print_works_ids.write({
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
                    'depend_selling_price': line.selling_price,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                })
            )
        aula_lst = []
        for line in self.service_type_id.aula_line_ids:
            aula_lst.append(
                (0, 0, {
                    'description': line.description,
                    'qty': line.qty,
                    'depend_selling_price': line.selling_price,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                })
            )
        print_works_lst = []
        for line in self.service_type_id.print_works_line_ids:
            print_works_lst.append(
                (0, 0, {
                    'description': line.description,
                    'qty': line.qty,
                    'depend_selling_price': line.selling_price,
                    'variant_id': line.variant_id.ids,
                    'product_id': line.product_id.id,
                })
            )
        # self.write({'funeral_service_line_id': lst})
        self.write({
            'funeral_service_line_id': lst,
            'funeral_aula_ids': aula_lst,
            'funeral_print_works_ids': print_works_lst,
        })

    @api.depends('funeral_service_line_id')
    def get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_service_line_id:
                line_price = rec.funeral_service_line_id.mapped(
                    'price')
                total = sum(line_price)
                # if rec.supplement_out_of_hours == "yes":
                #     total += rec.service_type_id.supplement_out_of_hours_price
                rec.amount_untaxed = total
                rec.amount_tax = (total * 6) / 100
                rec.amount_total = rec.amount_untaxed + rec.amount_tax

    @api.depends('funeral_aula_ids')
    def aula_get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_aula_ids:
                line_price = rec.funeral_aula_ids.mapped(
                    'price')
                total = sum(line_price)
                rec.aula_amount_untaxed = total
                rec.aula_amount_tax = (total * 6) / 100
                rec.aula_amount_total = rec.aula_amount_untaxed + rec.aula_amount_tax

    @api.depends('funeral_print_works_ids')
    def aula_get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_print_works_ids:
                line_price = rec.funeral_print_works_ids.mapped(
                    'price')
                total = sum(line_price)
                rec.print_works_amount_untaxed = total
                rec.print_works_amount_tax = (total * 6) / 100
                rec.print_works_amount_total = rec.print_works_amount_untaxed + rec.print_works_amount_tax


class FuneralServiceLine(models.Model):
    _name = 'funeral.service.line'
    _description = 'Funeral Service Line'

    def _default_domain_variant_ids(self):
        product_ids = self.env['product.template'].search([])
        value_ids = product_ids.mapped('attribute_line_ids').mapped('value_ids')
        return [('id', 'in', value_ids.ids)]

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    product_id = fields.Many2one('product.template')
    description = fields.Char(related="product_id.display_name", readonly=False)
    qty = fields.Float()
    variant_id = fields.Many2many('product.attribute.value', domain=lambda self: self._default_domain_variant_ids())
    depend_selling_price = fields.Float(related="product_id.list_price")
    price = fields.Float(store=True, compute="_get_selling_price")

    @api.depends('qty', 'variant_id')
    def _get_selling_price(self):
        for rec in self:
            rec.price = (rec.qty * (rec.depend_selling_price + sum(rec.variant_id.mapped('variant_price'))))


class FuneralAula(models.Model):
    _name = 'funeral.aula'
    _description = 'Funeral Aula'

    def _default_domain_variant_ids(self):
        product_ids = self.env['product.template'].search([])
        value_ids = product_ids.mapped('attribute_line_ids').mapped('value_ids')
        return [('id', 'in', value_ids.ids)]

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    description = fields.Char(related="product_id.display_name", readonly=False)
    product_id = fields.Many2one('product.template')
    qty = fields.Float()
    variant_id = fields.Many2many('product.attribute.value', domain=lambda self: self._default_domain_variant_ids())
    depend_selling_price = fields.Float(related="product_id.list_price")
    price = fields.Float(store=True, compute="_get_selling_price")

    @api.depends('qty', 'variant_id')
    def _get_selling_price(self):
        for rec in self:
            rec.price = (rec.qty * (rec.depend_selling_price + sum(rec.variant_id.mapped('variant_price'))))


class FuneralPrintWorks(models.Model):
    _name = 'funeral.print.works'
    _description = 'Funeral Print Works'

    def _default_domain_variant_ids(self):
        product_ids = self.env['product.template'].search([])
        value_ids = product_ids.mapped('attribute_line_ids').mapped('value_ids')
        return [('id', 'in', value_ids.ids)]

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    description = fields.Char(related="product_id.display_name", readonly=False)
    product_id = fields.Many2one('product.template')
    qty = fields.Float()
    variant_id = fields.Many2many('product.attribute.value', domain=lambda self: self._default_domain_variant_ids())
    depend_selling_price = fields.Float(related="product_id.list_price")
    price = fields.Float(store=True, compute="_get_selling_price")

    @api.depends('qty', 'variant_id')
    def _get_selling_price(self):
        for rec in self:
            rec.price = (rec.qty * (rec.depend_selling_price + sum(rec.variant_id.mapped('variant_price'))))
