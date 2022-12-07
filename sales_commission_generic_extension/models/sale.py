# -*- coding: utf-8 -*-
# Copyright (C) 2018
# @author Carlos A. Garcia

from odoo import api, fields, models, tools, _
import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user, required=True, readonly=True, states={'draft': [('readonly', False)],'sent': [('readonly', False)] })

    def get_sales_team_commission(self, commission_brw, order):
        '''This method calculates sales team margin commission.
           @return : Id of created commission record.'''
        invoice_commission_ids = []
        invoice_commission_obj = self.env['invoice.sale.commission']
        team_goal = order.team_id.invoiced_target
        team_current = order.team_id.invoiced
        amount = order.amount_untaxed

        if (team_current >= team_goal):
            commission_amount = amount * (commission_brw.team_goal_commission / 100)
            name = 'Comisión "' + tools.ustr(commission_brw.name) +' (' + tools.ustr(commission_brw.team_goal_commission) + '%)"' + ' por cumplimiento de meta de Equipo de Ventas'
            invoice_commission_data = {
                               'name': name,
                               'user_id' : order.user_id.id,
                               'order_id' : order.id,
                               'commission_id' : commission_brw.id,
                               'type_name' : commission_brw.name,
                               'comm_type' : commission_brw.comm_type,
                               'commission_amount' : commission_amount,
                               'date':datetime.datetime.today()
                               }
            invoice_commission_ids.append(invoice_commission_obj.create(invoice_commission_data))
        return invoice_commission_ids

    # @api.multi
    def get_sales_commission(self):
        '''This is control method for calculating commissions(called from workflow).
           @return : List of ids for commission records created.'''
        for order in self:
            invoice_commission_ids = []
            if order.user_id :
                commission_obj = self.env['sale.commission']
                commission_id = commission_obj.search([('user_ids', 'in', order.user_id.id)])
                if not commission_id:return False
                else:
                    commission_id = commission_id[0]
                commission_brw = commission_id
                
                if commission_brw.comm_type == 'mix':
                    invoice_commission_ids = self.get_mix_commission(commission_brw, order)
                elif commission_brw.comm_type == 'partner':
                    invoice_commission_ids = self.get_partner_commission(commission_brw, order)
                elif commission_brw.comm_type == 'discount':
                    invoice_commission_ids = self.get_discount_commission(commission_brw, order)
                elif commission_brw.comm_type == 'sales_team':
                    invoice_commission_ids = self.get_sales_team_commission(commission_brw, order)
                else:
                    invoice_commission_ids = self.get_standard_commission(commission_brw, order)
        return invoice_commission_ids

    # @api.multi
    @api.onchange('user_id')
    def onchange_salesperson(self):
        """
        on_change handler of user_id.
        """
        team_ids = self.env['crm.team'].search(['|',('member_ids.id','=',self.user_id.id),('user_id','=',self.user_id.id)])
        if not team_ids or (team_ids and len(team_ids) > 1):
          self.team_id = False
        else:
          self.team_id = team_ids[0]

    # @api.multi
    # def action_invoice_create(self):
    #     if len(self.commission_ids) > 0:
    #         self.commission_ids[0].write({'invoiced': True})
    #     return super(SaleOrder, self).action_invoice_create()

    def get_sales_team_commission_by_product(self, commission_brw, order):
        '''This method calculates sales team margin commission by product line.
           @return : Id of created commission record.'''
        invoice_commission_ids = []
        invoice_commission_obj = self.env['invoice.sale.commission']
        team_goal = order.team_id.invoiced_target
        team_current = order.team_id.invoiced

        for line in order.order_line:
            amount = line.price_subtotal
            if (team_current >= team_goal):
                commission_amount = amount * (commission_brw.team_goal_commission / 100)
                name = 'Comisión "' + tools.ustr(commission_brw.name) +' ( ' + tools.ustr(commission_brw.team_goal_commission) + '%)"' + ' por cumplimiento de meta de Equipo de Ventas'
                # name = 'Comisión por cumplimineto de meta de Equipo de Ventas" '+ tools.ustr(commission_brw.name) +' ( ' + tools.ustr(commission_brw.team_goal_commission) + '%)" for product "' + tools.ustr(line.product_id.name) + '"'
                standard_invoice_commission_data = {
                                   'name': name,
                                   'user_id' : order.user_id.id,
                                   'commission_id' : commission_brw.id,
                                   'product_id' : line.product_id.id,
                                   'type_name' : commission_brw.name,
                                   'comm_type' : commission_brw.comm_type,
                                   'commission_amount' : commission_amount,
                                   'order_id' : order.id,
                                   'date':datetime.datetime.today()
                                   }
                invoice_commission_ids.append(invoice_commission_obj.create(standard_invoice_commission_data))
        return invoice_commission_ids