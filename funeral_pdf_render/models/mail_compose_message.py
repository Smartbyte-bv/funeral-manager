from odoo import fields, models, api, _


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.onchange('template_id')
    def _onchange_template_id_wrapper(self):
        if self._context.get('from_funeral', False):
            return
        return super(MailComposeMessage, self)._onchange_template_id_wrapper()
