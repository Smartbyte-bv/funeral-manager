from odoo import fields, models, api, _
import fitz


class SignItem(models.Model):
    _inherit = 'sign.item'

    font_size = fields.Integer(default=11)
    font_name = fields.Char(default="helv")
