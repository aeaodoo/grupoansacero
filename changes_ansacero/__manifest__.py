# -*- coding: utf-8 -*-
{
    'name': "changes_ansacero",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'contacts', 'account_accountant', 'account','fleet','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_form_view.xml',
        'views/product_template_form_view.xml',
        'views/colony_catalogues_views.xml',
        'views/fleet_vehicle_form_view.xml',
        'views/sale_orde_form_view.xml',
        'reports/report_cotizacion_orden.xml',
        "reports/template_ticket.xml",
        "reports/report_ticket.xml",
        'views/stock_picking_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
