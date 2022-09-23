import base64
import datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import config
from PyPDF2 import PdfFileReader

import decimal
import io
import os
import fitz

FORMAT_DATETIME = '%d-%m-%Y %H:%M:%S'
FORMAT_DATE = '%d-%m-%Y'


class SignTemplate(models.Model):
    _inherit = 'sign.template'

    def get_field_list_in_template(self):
        res = []
        for item in self.sign_item_ids:
            data = {
                'field': item.type_id.auto_field,
                'required': item.required,
                'responsible_id': item.responsible_id.name,
                'page': item.page,
                'posX': item.posX,
                'posY': item.posY,
                'width': item.width,
                'height': item.height,
                'align': item.alignment
            }
            res.append(data)

        return res

    def pdf_resolution(self, path):
        with io.open(path, mode="rb") as f:
            input_pdf = PdfFileReader(f)
            media_box = input_pdf.getPage(0).mediaBox

        min_pt = media_box.lowerLeft
        max_pt = media_box.upperRight

        pdf_width = max_pt[0] - min_pt[0]
        pdf_height = max_pt[1] - min_pt[1]
        return pdf_width, pdf_height

    def prepare_vals_to_create_attachment(self, file_name, data, res_id, model):
        return {
            'name': file_name,
            'datas': data,
            'store_fname': file_name,
            'res_model': model,
            'template_id': self.id,
            'res_id': res_id
        }

    def create_attachment_file(self, file_name, data, res_id, model):
        vals = self.prepare_vals_to_create_attachment(file_name, data, res_id, model)
        attachment_id = self.env['ir.attachment'].create(vals)
        return attachment_id.id

    def generate_file(self, case_id, model):
        """

        @param case_id:
        @param model:
        @return:
        """
        self.ensure_one()

        input_path = self.attachment_id._full_path(self.attachment_id.store_fname)
        doc = fitz.open(input_path)
        if not doc:
            raise ValidationError("PDF file does not exist in the system!")

        data = self.get_field_list_in_template()
        pdf_width, pdf_height = self.pdf_resolution(input_path)
        for item in data:
            index_x = item['posX']
            index_y = item['posY']

            width = item['width']
            height = item['height']

            page = doc[item['page'] - 1]
            page.wrap_contents()

            rect_x1 = float(decimal.Decimal(index_x) * pdf_width)
            rect_y1 = float(decimal.Decimal(index_y) * pdf_height)
            rect_x2 = float(decimal.Decimal((index_x + width)) * pdf_width)
            rect_y2 = float(decimal.Decimal((index_y + height)) * pdf_height)

            rect = (rect_x1, rect_y1, rect_x2, rect_y2)
            text = item['field']

            font_size = 10
            font_name = "helv"
            generate_text = eval('case_id.{}'.format(text)) if text else ''

            if isinstance(generate_text, datetime.datetime):
                generate_text = generate_text.strftime(FORMAT_DATETIME)
            if isinstance(generate_text, datetime.date):
                generate_text = generate_text.strftime(FORMAT_DATE)
            if isinstance(generate_text, bool):
                if generate_text:
                    generate_text = 'v'
                else:
                    generate_text = ''

            page.insert_textbox(rect, generate_text, fontname=font_name, fontsize=font_size, align=item['align'])

        path = os.path.join(config.get('data_dir'), "tmp/")
        if not os.path.exists(path):
            os.mkdir(path, 0o777)

        file_name = "{} {}".format(case_id.partner_id.name, self.name)
        new_doc_path = "{}/{}".format(path, file_name)
        doc.save(new_doc_path)

        with open(new_doc_path, "rb") as f:
            data = base64.b64encode(f.read())

        attachment_id = self.create_attachment_file(file_name, data, case_id.partner_id.id, model)
        return attachment_id
