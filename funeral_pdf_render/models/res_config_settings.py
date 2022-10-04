from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    config_tags = fields.Boolean(string="Funeral document tag:")
    tag_ids = fields.Many2many('sign.template.tag')
    deceased_tag_ids = fields.Many2many('res.partner.category', 'res_config_setting_deceased_tag_rel')
    doctor_tag_ids = fields.Many2many('res.partner.category', 'res_config_setting_doctor_tag_rel')

    @api.model
    def get_values(self):
        res = super().get_values()

        model = self.env['service.type.document']

        list_tags = self.env['ir.config_parameter'].sudo().get_param('funeral_pdf_render.list_tags')
        list_deceased_tag = self.env['ir.config_parameter'].sudo().get_param('funeral_pdf_render.list_deceased_tags')
        list_doctor_tag = self.env['ir.config_parameter'].sudo().get_param('funeral_pdf_render.list_doctor_tags')

        tag_ids = model.get_tag_ids_from_list(list_tags, model='sign.template.tag')
        deceased_tag_ids = model.get_tag_ids_from_list(list_deceased_tag, model='res.partner.category')
        doctor_tag_ids = model.get_tag_ids_from_list(list_doctor_tag, model='res.partner.category')

        res.update(
            config_tags=self.env['ir.config_parameter'].sudo().get_param('funeral_pdf_render.config_tags'),
            tag_ids=tag_ids,
            deceased_tag_ids=deceased_tag_ids,
            doctor_tag_ids=doctor_tag_ids,
        )
        return res

    def get_list_tags(self, tag_ids):
        if not tag_ids:
            return False
        return ', '.join(tag_ids.mapped('name'))

    def set_values(self):
        res = super().set_values()

        param = self.env['ir.config_parameter'].sudo()

        list_tags = self.get_list_tags(self.tag_ids)
        list_deceased_tags = self.get_list_tags(self.deceased_tag_ids)
        list_doctor_tags = self.get_list_tags(self.doctor_tag_ids)

        param.set_param('funeral_pdf_render.config_tags', self.config_tags)
        param.set_param('funeral_pdf_render.list_tags', list_tags)
        param.set_param('funeral_pdf_render.list_deceased_tags', list_deceased_tags)
        param.set_param('funeral_pdf_render.list_doctor_tags', list_doctor_tags)

        return res
