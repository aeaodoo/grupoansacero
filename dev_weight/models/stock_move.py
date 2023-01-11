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


class StockMove(models.Model):
    _inherit = 'stock.move'

    def get_product_weight_global(self):
        for line in self:
            weight = 0
            if line.product_id and line.product_id.weight:
                weight = line.product_id.weight * line.product_uom_qty
            line.product_weight_global = weight

    product_weight_global = fields.Float(string='Weight(kg)', compute='get_product_weight_global')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: