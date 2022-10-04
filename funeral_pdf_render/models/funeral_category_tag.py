from odoo import fields, models, api, _


class FuneralCategoryTag(models.Model):
    _name = 'funeral.category.tag'

    name = fields.Char()
    tag_ids = fields.Many2many('res.partner.category')
