{
    'name': 'Funeral Management System',
    'summary': 'Funeral Management System.',
    'description': 'Funeral Management System.',
    'version': '15.0.1.0.1',
    'author': 'Tecspek',
    'depends': [
        'base', 'mail', 'contacts', 'sale_management'
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/funeral_management_view.xml',
        'views/service_type_view.xml',
        # 'views/service_variant_view.xml',
        'views/product_category_view.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'live_test_url': '',
}
