from odoo import fields, models, api, _


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    template_id = fields.Many2one('sign.template')
