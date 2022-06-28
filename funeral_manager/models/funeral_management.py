from odoo import fields, models, api, _


class FuneralManagement(models.Model):
    _name = 'funeral.management'
    _description = 'FuneralManagement'
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
    supplement_out_of_hours = fields.Selection([('no', 'No'), ('yes', 'Yes')],
                                               string="Supplement Saturday/out of hours", default="no",
                                               related="service_type_id.supplement_out_of_hours", readonly=False)
    product_product_1 = fields.Many2one('product.product', domain=lambda self: self._default_domain_variant_1_ids(),
                                        related="service_type_id.product_product_1", readonly=False)
    product_product_2 = fields.Many2one('product.product', domain=lambda self: self._default_domain_variant_2_ids(),
                                        related="service_type_id.product_product_2", readonly=False)
    product_product_3 = fields.Many2one('product.product', domain=lambda self: self._default_domain_variant_3_ids(),
                                        related="service_type_id.product_product_3", readonly=False)
    product_product_1_price = fields.Float(related="product_product_1.list_price")
    product_product_2_price = fields.Float(related="product_product_2.list_price")
    product_product_3_price = fields.Float(related="product_product_3.list_price")
    amount_untaxed = fields.Float(store=True, compute="get_total_price")
    amount_tax = fields.Float(store=True, compute="get_total_price")
    amount_total = fields.Float(store=True, compute="get_total_price")

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
            # self.write({
            #     'funeral_service_line_id': [(6, 0, self.funeral_service_line_id.ids)]
            # })
        lst = []
        for line in self.service_type_id.line_ids:
            lst.append(
                (0, 0, {
                    'select_service': True,
                    'description': line.description,
                    'qty': line.qty,
                    'depend_selling_price': line.selling_price,
                })
            )
        self.write({'funeral_service_line_id': lst})

    @api.depends('product_product_1', 'product_product_2', 'product_product_3', 'supplement_out_of_hours',
                 'funeral_service_line_id')
    def get_total_price(self):
        for rec in self:
            total = 0.0
            if rec.funeral_service_line_id:
                line_price = rec.funeral_service_line_id.filtered(lambda r: r.select_service).mapped(
                    'price')
                total = sum(line_price)
                if rec.supplement_out_of_hours == "yes":
                    total += rec.service_type_id.supplement_out_of_hours_price
                if rec.product_product_1:
                    total += rec.product_product_1.list_price
                if rec.product_product_2:
                    total += rec.product_product_2.list_price
                if rec.product_product_3:
                    total += rec.product_product_3.list_price
                rec.amount_untaxed = total
                rec.amount_tax = (total * 6) / 100
                rec.amount_total = rec.amount_untaxed + rec.amount_tax


class FuneralServiceLine(models.Model):
    _name = 'funeral.service.line'
    _description = 'Funeral Service Line'

    funeral_id = fields.Many2one('funeral.management')
    service_type_id = fields.Many2one('service.type', related="funeral_id.service_type_id")
    description = fields.Char()
    qty = fields.Float()
    depend_selling_price = fields.Float()
    price = fields.Float(store=True, compute="_get_selling_price")
    select_service = fields.Boolean()

    @api.depends('qty')
    def _get_selling_price(self):
        for rec in self:
            rec.price = rec.qty * rec.depend_selling_price
            print(">>>>>dsad", rec.qty)
            print(">>>>>dsad", rec.depend_selling_price)
            print(">>>>>dsad", rec.price)

# class ServiceVariant(models.Model):
#     _name = 'service.variant'
#     _description = 'Service Variant'
#
#     name = fields.Char()
#     price = fields.Float()
