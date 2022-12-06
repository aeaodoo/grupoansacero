# from openerp.addons.l10n_mx_invoice_amount_to_text import amount_to_text_es_MX
from odoo import _, api, fields, models, tools
from odoo.tools import float_round
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_repr

class SaleOrderTicketReport(models.AbstractModel):
    # _name must be report.module_name.template_id
    _name = 'changes_ansacero.sale_order_ticket_pdf'

    def _get_amount_to_text(self, order):
        """Method to transform a float amount to text words
        E.g. 100 - ONE HUNDRED
        :returns: Amount transformed to words mexican format for invoices
        :rtype: str
        """
        # self.ensure_one()
        currency = order.currency_id.name.upper()
        # M.N. = Moneda Nacional (National Currency)
        # M.E. = Moneda Extranjera (Foreign Currency)
        currency_type = 'M.N.' if currency == 'MXN' else 'M.E.'
        # Split integer and decimal part
        amount_i, amount_d = divmod(order.amount_total, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))
        words = order.currency_id.with_context(lang=order.partner_id.lang or 'es_ES').amount_to_text(amount_i).upper()
        order_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
            words=words, amount_d=amount_d, curr_t=currency_type)
        return order_words
        # return "Words!!"+ str(currency)+ str(order.amount_total)

    def get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'get_amount_to_text': self._get_amount_to_text(docs),
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'data': data,
            'docs': docs,
        }

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('report_ticket_pdf.changes_ansacero_order_ticket_pdf')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('report_ticket_pdf.changes_ansacero_order_ticket_pdf', docargs)