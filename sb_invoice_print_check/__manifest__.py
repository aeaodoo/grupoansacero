# -*- coding: utf-8 -*-
{
    'name': "Invoice Print Check",

    'summary': """
        Verifica el estado de impresión de las Facturas de clientes.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Josué Flores Osorio [josueflores.05@gmail.com]",
    'website': "https://smart-business.co/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'post_init_hook': '_verify_invoice_attachment',
}
