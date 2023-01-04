# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

def _verify_invoice_attachment(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    attachments = env['ir.attachment']
    
    # Search invoice
    invoices_partner = env['account.move'].search([('move_type','=','out_invoice')])
    for invoice in invoices_partner.filtered(lambda inv: inv.message_attachment_count > 0):
        count = attachments.search([('res_model','=','account.move'), ('res_id','=',invoice.id),
                                        ('name','ilike',"%.pdf")], count=True) # Only PDF files.
        if count > 0:
            invoice.printed = True