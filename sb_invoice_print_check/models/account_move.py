# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    printed = fields.Boolean(string='Impresa', default=False)


class AccountInvoiceSendInherit(models.TransientModel):
     _inherit = 'account.invoice.send'
     
     
     def send_and_print_action(self):
        res = super(AccountInvoiceSendInherit, self).send_and_print_action()
        if self.is_print:
            self.mapped('invoice_ids').sudo().write({'printed': True})
        return res
    