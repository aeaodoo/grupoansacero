# -*- coding: utf-8 -*-
# Copyright (C) 2018
# @author Carlos A. Garcia

from odoo import api, fields, models, tools, _
import logging
_logger = logging.getLogger(__name__)


class CrmTeam(models.Model):
    _inherit = "crm.team"
    _description = "Add commission field to the sales team."

    commission_id = fields.Many2one('sale.commission', string='Comisión', compute='_get_commission', help='Comisión del Equipo de venta.')

    # @api.multi
    def _get_commission(self):
        '''This method find the commission assigned to the sales team.
           @return : commission record.'''
        commission_obj = self.env['sale.commission']
        commission_id = commission_obj.search([('sales_team', '=', self.id)])
        # _logger.info('@@@ commission_id ID=%i - %s selected :::::',commission_id.id, commission_id.name)
        if not commission_id:
            self.commission_id = False
        else:
            self.commission_id = commission_id

        return commission_id