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

        'views/sign_template.xml',
        'views/res_partner.xml',
        'views/funeral_management.xml',
        'wizard/sign_template_render.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {"python": ['PyMuPDF==1.20.2']}
}
