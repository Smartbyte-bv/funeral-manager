from odoo import fields, models, api, _


class FuneralManagement(models.Model):
    _inherit = 'funeral.management'

    def action_open_generate_form(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Generate Template',
            'view_mode': 'form',
            'res_model': 'sign.template.render',
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_order_id': self.partner_id.order_id.id,
            },
        }
