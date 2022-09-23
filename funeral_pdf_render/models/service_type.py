from odoo import fields, models, api, _


class ServiceType(models.Model):
    _inherit = 'service.type'

    document_ids = fields.One2many('service.type.document', 'type_id')


class ServiceTypeDocument(models.Model):
    _name = 'service.type.document'

    type_id = fields.Many2one('service.type')
    template_id = fields.Many2one('sign.template')
    attachment_ids = fields.Many2many('ir.attachment')
    description = fields.Text()
