# -*- coding: utf-8 -*-
# Copyright (C) 2018
# @author Carlos A. Garcia

from odoo import api, fields, models, tools, _
from odoo.fields import datetime
from datetime import timedelta

import logging
_logger = logging.getLogger(__name__)

class SaleCommission(models.Model):
    _inherit = "sale.commission"
    _rec_name = 'name'
    _description = "Add a new type of comission based on sales team target."

    active = fields.Boolean('Activo', default=True)
    team_id = fields.Many2one('crm.team', string='Equipo de Ventas', help='Equipo de venta con la meta a alcanzar.')
    team_goal_commission = fields.Float(string="Porcentaje", help="Porciento de comisión de Equipo de Ventas")
    comm_type = fields.Selection([
        ('standard', 'Standard'),
        ('partner', 'Partner Based'),
        ('mix', 'Product/Category/Margin Based'),
        ('sales_team', 'Objetivo de Ventas'),
        ('discount', 'Discount Based'),
        ], 'Commission Type', copy=False, default= 'standard', help="Select the type of commission you want to apply.")

    # team_goal = fields.Integer(string='Meta', store=False, related='team_id.invoiced_target', readonly=True)
    # team_current = fields.Integer(string='Actual', store=False, compute='compute_total', default=0)
    team_current = fields.Char(string='Facturación Equipo', store=False, compute='compute_total')

    def compute_total(self):
        # if self.team_id.invoiced and self.team_id.invoiced > 0:
        #     self.team_current = self.team_id.invoiced
        #     return self.team_current
        # else:
        #     return 0
        self.team_current = str('$ ') + str(self.team_id.invoiced) + ' / ' + str(self.team_id.invoiced_target)

    def _check_uniqueness_sales_team(self):
        '''This method checks constraint for only one commission group for each sales person'''
        for obj in self:
            ex_ids = self.search([('team_id', 'in', [x.id for x in obj.team_id])])
            if len(ex_ids) > 1:
                return False
        return True

    _constraints = [
        (_check_uniqueness_sales_team, '¡Sólo se puede configurar una comisión por Equipo de ventas!', ['team_id']),
    ]

    @api.onchange('team_id')
    def onchange_team_id(self):
        """
        on_change handler of team_id.
        """
        for obj in self:
            obj.team_current = str('$ ') + str(obj.team_id.invoiced) + ' / ' + str(obj.team_id.invoiced_target)

            if obj.team_id:
                users = self.env['res.users'].search([('id','in',obj.team_id.member_ids.ids)])
                relation_ids = [x.id for x in users]
                domain = {'user_ids':[('id','in',relation_ids)]}
            else:            
                users = self.env['res.users'].search([('active','=',True)])
                relation_ids = [x.id for x in users]
                domain = {'user_ids':[('id','in',relation_ids)]}
        return {'domain':domain}

    @api.onchange('comm_type')
    def onchange_comm_type(self):
        """
        on_change handler of comm_type.
        """
        self.team_id = False

class InvoiceSaleCommission(models.Model):
    _inherit = "invoice.sale.commission"
    _description = "Add a new type of comission based on sales team target."

    comm_type = fields.Selection([
        ('standard', 'Standard'),
        ('partner', 'Partner Based'),
        ('mix', 'Product/Category/Margin Based'),
        ('sales_team', 'Objetivo de Ventas'),
        ('discount', 'Discount Based'),
        ], 'Commission Type', copy=False, help="Select the type of commission you want to apply.")

    # @api.one
    def compute_state(self):
        for record in self:
            if record.invoice_id:
                if record.invoice_id.team_id.invoiced >= record.invoice_id.team_id.invoiced_target:
                    record.approved = True
            elif record.order_id:
                if record.order_id.team_id.invoiced >= record.order_id.team_id.invoiced_target:
                    record.approved = True

    # @api.one
    @api.depends('date')
    def compute_period(self):
        for record in self:
            print("Imprimiendo fecha de factura: ", record.date)
            #record.period = datetime.strptime(record.date,"%Y-%m-%d").strftime("%m/%Y")
            record.period = datetime.strptime(record.date.strftime("%m/%Y"), '%m/%Y')

    approved = fields.Boolean('Aprobada', store=False, compute='compute_state', default=False)
    #period = fields.Char(string='Período', store=True, default= datetime.today().strftime("%m/%Y")) # important declare the method first the 'default=' in field.
    period = fields.Char(string='Período', store=True, compute='compute_period')