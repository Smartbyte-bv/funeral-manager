# -*- coding: utf-8 -*-

{
    'name': 'Funeral PDF Render',
    'version': '15.0',
    'sequence': 2,
    'summary': 'Funeral PDF Render',
    'description': "Render PDF File For Funeral",
    'depends': ['funeral_manager', 'sign'],
    'data': [
        'security/funeral_security.xml',
        'security/ir.model.access.csv',
        'data/sign_item_type_data.xml',
        'data/sign_item_type_data.xml',
        'data/mail_template_data.xml',
        'data/funeral_category_tag.xml',

        'views/res_partner.xml',
        'views/service_type.xml',
        'views/funeral_management.xml',
        'views/res_partner_type.xml',
        'views/res_config_settings.xml',
        'views/sign_template.xml',
        'views/funeral_category_tag.xml',

        'wizard/sign_template_render.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {"python": ['PyMuPDF==1.20.2']}
}
