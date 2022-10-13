from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    order_id = fields.Many2one('sale.order')

    def _default_category(self):
        if self.env.context.get('create_from_funeral'):
            return self.env['res.config.settings'].sudo().search([('company_id',"=", self.env.company.id)]).deceased_tag_ids
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    category_id = fields.Many2many('res.partner.category', column1='partner_id',
                                    column2='category_id', string='Tags', default=_default_category)