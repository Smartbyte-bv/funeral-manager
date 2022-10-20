from odoo import models, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    funeral_id = fields.Many2one('funeral.management')


    def action_view_funeral(self):
        self.ensure_one()
        return {
            'name': _('Funeral Management'),
            'view_mode': 'form',
            'res_model': 'funeral.management',
            'res_id': self.funeral_id.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
        }
    
