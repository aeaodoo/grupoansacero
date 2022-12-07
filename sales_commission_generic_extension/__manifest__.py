# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Adaptaciones para módulo de Comisiones',
    'version': '1.2',
    'category': 'Extensión',
    'author': "Carlos A. García",
    'website': "http://www.ikom.mx",
    'summary': 'Extensión del módulo: "sales_commission_generic"',
    'description': """
    """,
    'depends': [
        'sales_commission_generic',
    ],
    'external_dependencies' : {
        # 'python' : ['OpenSSL'],
    },
    'data': [
        'views/sale_config_settings.xml',
        'views/sale_commission_view.xml',
        # 'views/crm_team_view.xml',
        'views/sale_order_view.xml',
        'views/invoice_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    # "post_init_hook": "post_init_hook",
    'installable': True,
    'auto_install': False,
}
