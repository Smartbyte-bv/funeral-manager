from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    config_tags = fields.Boolean()
    tag_ids = fields.Many2many('sign.template.tag')

    @api.model
    def get_values(self):
        res = super().get_values()

        list_tags = self.env['ir.config_parameter'].sudo().get_param('funeral_pdf_render.list_tags')
        tag_ids = self.env['service.type.document'].get_tag_ids_from_list(list_tags)

        res.update(
            config_tags=self.env['ir.config_parameter'].sudo().get_param('funeral_pdf_render.config_tags'),
            tag_ids=tag_ids
        )
        return res

    def get_list_tags(self):
        if not self.tag_ids:
            return False
        return ', '.join(self.tag_ids.mapped('name'))

    def set_values(self):
        res = super().set_values()

        param = self.env['ir.config_parameter'].sudo()

        list_tags = self.get_list_tags()

        param.set_param('funeral_pdf_render.config_tags', self.config_tags)
        param.set_param('funeral_pdf_render.list_tags', list_tags)

        return res
