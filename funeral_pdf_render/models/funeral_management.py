from odoo import fields, models, api, _

WEEK_DATA = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}
selection_option = [('yes', 'Yes'), ('no', 'No')]

TEMPLATE_FIELDS_DICT = {
    'service_type': {'name': 'Service Type', 'value': 'service_type', 'type': 'text'},
    'name': {'name': 'Partner Name', 'value': 'name', 'type': 'text'},
    'responsible_service': {'name': 'Responsible Service', 'value': 'responsible_service', 'type': 'text'},
    'dod': {'name': 'Date of Death', 'value': 'dod', 'type': 'text'},
    'dob': {'name': 'Date of Birth', 'value': 'dob', 'type': 'text'},
    'rk_number': {'name': 'RK Number', 'value': 'rk_number', 'type': 'text'},
    'place_of_birth': {'name': 'Place of Birth', 'value': 'place_of_birth', 'type': 'text'},
    'place_of_death': {'name': 'Place of Death', 'value': 'place_of_death', 'type': 'text'},
    'last_address': {'name': 'Last Address', 'value': 'last_address', 'type': 'text'},
    'doctor_id': {'name': 'Doctor', 'value': 'doctor_id.name', 'type': 'text'},
    'law_doctor_id': {'name': 'Law Doctor', 'value': 'law_doctor_id.name', 'type': 'text'},
    'transferred_on': {'name': 'Transferred On', 'value': 'transferred_on', 'type': 'text'},
    'picked_up': {'name': 'Picked Up', 'value': 'picked_up', 'type': 'text'},
    'is_dress': {'name': 'Dress', 'value': 'is_dress', 'type': 'checkbox'},
    'is_statement': {'name': 'Statement', 'value': 'is_statement', 'type': 'checkbox'},
    'spouse_id': {'name': 'Spouse', 'value': 'spouse_id.name', 'type': 'text'},
    'widow_id': {'name': 'Widow', 'value': 'widow_id.name', 'type': 'text'},
    'father_id': {'name': 'Father', 'value': 'father_id.name', 'type': 'text'},
    'mother_id': {'name': 'Mother', 'value': 'mother_id.name', 'type': 'text'},
    'partner_id': {'name': 'Partner', 'value': 'partner_id.name', 'type': 'text'},
    'minor': {'name': 'Minor', 'value': 'minor', 'type': 'text'},
    'of_age': {'name': 'of Age', 'value': 'of_age', 'type': 'text'},
    'father_deceased': {'name': 'Father Deceased', 'value': 'father_deceased', 'type': 'checkbox'},
    'mother_deceased': {'name': 'Mother Deceased', 'value': 'mother_deceased', 'type': 'checkbox'}
}


class FuneralManagement(models.Model):
    _inherit = 'funeral.management'

    related_document_ids = fields.Many2many('funeral.management.document')
    dob_weekday = fields.Char(compute='_compute_weekday', store=True)
    dod = fields.Date(string='Date Of Death')
    dod_weekday = fields.Char(compute='_compute_weekday', store=True)
    rk_number = fields.Char()
    place_of_birth = fields.Char()
    place_of_death = fields.Char()
    last_address = fields.Text()
    doctor_id = fields.Many2one('res.partner')
    law_doctor_id = fields.Many2one('res.partner')
    transferred_on = fields.Date()
    transferred_on_weekday = fields.Char(compute='_compute_weekday', store=True)
    picked_up = fields.Date()
    picked_up_weekday = fields.Char(compute='_compute_weekday', store=True)
    is_dress = fields.Selection(selection=selection_option)
    is_statement = fields.Selection(selection=selection_option)
    spouse_id = fields.Many2one('res.partner')
    widow_id = fields.Many2one('res.partner')
    father_id = fields.Many2one('res.partner')
    mother_id = fields.Many2one('res.partner')
    minor = fields.Integer()
    of_age = fields.Integer()
    father_deceased = fields.Boolean()
    mother_deceased = fields.Boolean()
    partner_type_id = fields.Many2one('res.partner.type')

    def build_dict_from_records(self, records):
        res = {}
        for rec in records:
            if rec.name not in res:
                res[rec.name] = []
            res[rec.name].append(rec)
        return res

    def get_existing_record(self, fields):
        domain = [('name', 'in', fields)]
        records = self.env['sign.item.type'].search(domain)
        record_dict = self.build_dict_from_records(records)
        return record_dict

    def get_list_field_name(self, fields):
        res = []
        for field in fields:
            res.append(TEMPLATE_FIELDS_DICT[field]['name'])
        return res

    def init(self):
        field_list = self.fields_get_keys()
        list_field_name = self.get_list_field_name(list(TEMPLATE_FIELDS_DICT.keys()))
        existing_record = self.get_existing_record(list_field_name)
        for field in field_list:
            if field not in TEMPLATE_FIELDS_DICT.keys():
                continue

            field_name = TEMPLATE_FIELDS_DICT[field]['name']
            is_existing = existing_record.get(field_name, False)
            if is_existing:
                continue

            val = {
                'name': TEMPLATE_FIELDS_DICT[field]['name'],
                'auto_field': TEMPLATE_FIELDS_DICT[field]['value'],
                'item_type': TEMPLATE_FIELDS_DICT[field]['type']
            }
            self.env['sign.item.type'].create(val)

    def get_weekday_by_date(self, date):
        if not date:
            return False

        weekday = date.weekday()
        return WEEK_DATA.get(weekday)

    @api.depends('dob', 'dod', 'transferred_on', 'picked_up')
    def _compute_weekday(self):
        for r in self:
            r.dob_weekday = r.get_weekday_by_date(r.dob)
            r.dod_weekday = r.get_weekday_by_date(r.dod)
            r.transferred_on_weekday = r.get_weekday_by_date(r.transferred_on)
            r.picked_up_weekday = r.get_weekday_by_date(r.picked_up)

    def action_open_generate_form(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Generate Template',
            'view_mode': 'form',
            'res_model': 'sign.template.render',
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_order_id': self.partner_id.order_id.id,
            },
        }

    def get_document_list_ids(self, documents):
        res_ids = []
        for document in documents:
            val = {
                'template_id': document.template_id.id,
                'partner_id': self.partner_id.id,
                'description': document.description
            }
            record_id = self.env['funeral.management.document'].create(val).id
            res_ids.append(record_id)

        return res_ids

    def unlink_existing_documents_without_case(self):
        domain = [('case_id', '=', self._origin.id)]
        documents = self.env['funeral.management.document'].search(domain)
        if documents:
            documents.unlink()

    @api.onchange('service_type_id')
    def _onchange_service_type(self):
        if not self.service_type_id:
            return

        documents = self.service_type_id.document_ids
        record_ids = self.get_document_list_ids(documents)

        self.related_document_ids = [(6, False, record_ids)]

    def update_case_id_to_documents(self):
        if self.related_document_ids:
            val = {'case_id': self.id}
            self.related_document_ids.write(val)

    @api.model
    def create(self, vals_list):
        res = super(FuneralManagement, self).create(vals_list)
        res.update_case_id_to_documents()
        self.unlink_existing_documents_without_case()
        return res

    def write(self, vals_list):
        res = super(FuneralManagement, self).create(vals_list)
        self.update_case_id_to_documents()
        return res


class FuneralManagementDocument(models.Model):
    _name = 'funeral.management.document'

    case_id = fields.Many2one('funeral.management')
    template_id = fields.Many2one('sign.template')
    partner_id = fields.Many2one('res.partner')
    description = fields.Text()
    attachment_id = fields.Many2one('ir.attachment')
    file = fields.Binary(related="attachment_id.datas")
    name = fields.Char(related="attachment_id.name")

    def action_create_document(self):
        case_id = self.case_id
        if not case_id:
            return

        partner = case_id.partner_id
        attachment_id = self.template_id.generate_file(case_id, partner._name)
        self.attachment_id = attachment_id

    def action_delete_document(self):
        case_id = self.case_id
        domain = [
            ('template_id', '=', self.template_id.id),
            ('res_model', '=', 'res.partner'),
            ('res_id', '=', case_id.partner_id.id)
        ]
        attachment = self.env['ir.attachment'].search(domain)
        if attachment:
            attachment.unlink()


class ResPartnerType(models.Model):
    _name = 'res.partner.type'

    name = fields.Char()
