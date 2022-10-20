from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    funeral_id = fields.Many2one('funeral.management', compute="_compute_funeral_id", store=True)

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

    @api.depends('invoice_line_ids.sale_line_ids')
    def _compute_funeral_id(self):
        for rec in self:
            rec.funeral_id = rec.invoice_line_ids.sale_line_ids.order_id.funeral_id
