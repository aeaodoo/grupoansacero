# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_total_product_weight_global(self):
        for picking in self:
            weight = 0
            if picking.move_lines:
                for line in picking.move_lines:
                    weight += line.product_weight_global
            picking.total_product_weight_global = weight

    total_product_weight_global = fields.Float(string='Weight', compute='get_total_product_weight_global')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: