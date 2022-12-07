# -*- coding: utf-8 -*-
# Copyright (C) 2018
# @author Carlos A. Garcia

from odoo import api, fields, models, tools, _
import datetime
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class WizardInvoiceSaleCommission(models.Model):
    _inherit = 'wizard.invoice.sale.commission'
    
    # @api.multi
    def print_commission_report(self):
        temp = []
        sale_invoice_commission_ids = self.env['invoice.sale.commission'].search([('date','>=',self.start_date),('date','<=',self.end_date),('user_id','=',self.salesperson.id)])
        if not sale_invoice_commission_ids:
            # raise Warning('There Is No Any Commissions.')
            raise ValidationError(_('No existen comisiones para el período y Usuario seleccionados.'))
        else:
            for a in sale_invoice_commission_ids:
                temp.append(a.id)
        data = temp
        datas = {
            'ids': self._ids,
            'model': 'invoice.sale.commission',
            'form': data,
            'start_date':self.start_date,
            'end_date':self.end_date,
            'user':self.salesperson.name
        }
#         return  self.env['report'].get_action(self, 'sales_commission_generic.sale_inv_comm_template', data=datas)
        return self.env.ref('sales_commission_generic.report_pdf').report_action(self,data=datas)


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def generate_commission(self, commission_brw, invoice, commission_amount):
        invoice_commission_ids = []
        invoice_commission_obj = self.env['invoice.sale.commission']
        team_goal = invoice.team_id.invoiced_target
        team_current = invoice.team_id.invoiced

        if (team_current >= team_goal):
            name = 'Comisión "' + tools.ustr(commission_brw.name) +' (' + tools.ustr(commission_brw.team_goal_commission) + '%)"' + ' por cumplimiento de meta de Equipo de Ventas'
            invoice_commission_data = {
                                   'name': name,
                                   'user_id' : invoice.user_id.id,
                                   'commission_id' : commission_brw.id,
                                   'type_name' : commission_brw.name,
                                   'comm_type' : commission_brw.comm_type,
                                   'commission_amount' : commission_amount,
                                   'invoice_id' : invoice.id,
                                   'date':datetime.datetime.today()}
            invoice_commission_ids.append(invoice_commission_obj.create(invoice_commission_data))

        return invoice_commission_ids


    def get_sales_team_commission(self, commission_brw, invoice):
        '''This method calculates sales team margin commission for invoices.
           @return : Id of created commission record.'''
        invoice_commission_ids = []
        amount = invoice.amount_untaxed

        #customer invoices
        if invoice.type == 'out_invoice':
            invoice_commission_amount = amount * (commission_brw.team_goal_commission / 100)
            invoice_commission_ids = self.generate_commission(commission_brw, invoice, invoice_commission_amount)
        #customer refund(credit notes)        
        elif invoice.type == 'out_refund':
            refund_commission_amount = (amount * (commission_brw.team_goal_commission / 100)) * -1               
            invoice_commission_ids = self.generate_commission(commission_brw, invoice, refund_commission_amount)

        return invoice_commission_ids

    # @api.multi
    def get_sales_commission(self):
        '''This inherits from parent method.
           @return : List of ids for commission records created.'''
        invoice_commission_ids = []
        for invoice in self:
            if invoice.user_id:
                commission_obj = self.env['sale.commission']
                commission_id = commission_obj.search([('user_ids', 'in', invoice.user_id.id)])
                if not commission_id:return False
                else:
                    commission_id = commission_id[0]
                commission_brw = commission_id
                
                if commission_brw.comm_type == 'mix':
                    invoice_commission_ids = self.get_mix_commission(commission_brw, invoice)
                elif commission_brw.comm_type == 'partner':
                    invoice_commission_ids = self.get_partner_commission(commission_brw, invoice)
                elif commission_brw.comm_type == 'discount':
                    invoice_commission_ids = self.get_discount_commission(commission_brw, invoice)
                elif commission_brw.comm_type == 'sales_team':
                    invoice_commission_ids = self.get_sales_team_commission(commission_brw, invoice)
                else:
                    invoice_commission_ids = self.get_standard_commission(commission_brw, invoice)

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