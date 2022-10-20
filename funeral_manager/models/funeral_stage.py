from odoo import fields, models, api


class FuneralStage(models.Model):
    _name = 'funeral.stage'
    _description = 'Funeral Stage'

    name = fields.Char(required=True)
    fold = fields.Boolean('Folded in Pipeline',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
