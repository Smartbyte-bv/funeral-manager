from odoo import fields, models, api, _


class ServiceType(models.Model):
    _inherit = 'service.type'

    document_ids = fields.One2many('service.type.document', 'type_id')


class ServiceTypeDocument(models.Model):
    _name = 'service.type.document'

    def get_tag_ids_from_list(self, list_tags):
        if not list_tags:
            return []

        list_tags = list_tags.split(', ')
        domain = [('name', 'in', list_tags)]
        tags = self.env['sign.template.tag'].search(domain)
        return tags.ids

    def get_domain_for_document_type(self):
        config_tags = self.env['ir.config_parameter'].sudo().get_param('funeral_pdf_render.config_tags')
        if not config_tags:
            return []

        list_tags = self.env['ir.config_parameter'].sudo().get_param('funeral_pdf_render.list_tags')
        tag_ids = self.get_tag_ids_from_list(list_tags)
        return [('tag_ids', 'in', tag_ids)]

    type_id = fields.Many2one('service.type')
    template_id = fields.Many2one('sign.template', domain=get_domain_for_document_type)
    attachment_ids = fields.Many2many('ir.attachment')
    description = fields.Text()
