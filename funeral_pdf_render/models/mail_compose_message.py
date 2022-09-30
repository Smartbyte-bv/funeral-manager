from odoo import fields, models, api, _


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.onchange('template_id')
    def _onchange_template_id_wrapper(self):
        res = super(MailComposeMessage, self)._onchange_template_id_wrapper()

        if self._context.get('from_funeral', False):
            attachment_ids = self._context.get('default_attachment_ids')
            current_attachment_ids = self.attachment_ids.ids
            record_ids = current_attachment_ids + attachment_ids
            self.attachment_ids = [(6, False, record_ids)]

        return res
