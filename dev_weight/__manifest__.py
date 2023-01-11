# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'All in One Weight- Sale, Purchase, Delivery Order',
    'version': '15.0.1.0',
    'sequence': 1,
    'category': 'Warehouse',
    'description':
        """
All in One Weight- Sale, Purchase, Delivery Order

Odoo application will automatically calculate total weight of products into Sale Order, Purchase Order and Delivery Order and show weight on every sale, purchase , delivery product lines.

        1.Calculate total weight of product into Sale Order\n
        2.Calculate total weight of product into Purchase Order\n
        3.Calculate total weight of product into Delivery Order\n

Key Features
\n
Calculate Weight of product per line in Sale Order Line
\n
Shows total weight of Products into Sale Order
\n
Calculate Weight of product per line in Purchase Order Line
\n
Shows total weight of Products into Purchase Order
\n
Calculate Weight of product per line in Delivery Order Line
\n
Shows total weight of Products into Delivery Order

Set Weight for each Product
Product Weight into Sale Order
Product Weight into Purchase Order
Product Weight into Delivery Order

    """,
    'summary': 'odoo app allow to add Weight Calculation of product on sale order line, purchase order line, delivery order, stcok move, sale weight, purchase weight, delivery weight, sale product weight, purchase product weight, delivery product weight, sale product line weight , purchase product line weight, stock product weight',
    'depends': ['sale_management', 'purchase', 'stock'],
    'data': [
        'views/sale_view.xml',
        'views/purchase_view.xml',
        'views/stock_picking_view.xml'
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':19.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
