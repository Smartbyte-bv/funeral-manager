from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    order_id = fields.Many2one('sale.order')
