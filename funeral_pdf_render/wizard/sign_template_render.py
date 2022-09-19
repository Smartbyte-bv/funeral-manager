from odoo import fields, models, api, _


class SignTemplateRender(models.Model):
    _name = 'sign.template.render'

    template_id = fields.Many2one('sign.template')
    partner_id = fields.Many2one('res.partner')
    order_id = fields.Many2one('sale.order')

    def action_generate_template_file(self):
        return self.template_id.generate_file(self.partner_id, self.order_id.id, self.order_id._name)
