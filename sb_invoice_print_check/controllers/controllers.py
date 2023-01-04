# -*- coding: utf-8 -*-
# from odoo import http


# class SbInvoicePrintCheck(http.Controller):
#     @http.route('/sb_invoice_print_check/sb_invoice_print_check', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sb_invoice_print_check/sb_invoice_print_check/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sb_invoice_print_check.listing', {
#             'root': '/sb_invoice_print_check/sb_invoice_print_check',
#             'objects': http.request.env['sb_invoice_print_check.sb_invoice_print_check'].search([]),
#         })

#     @http.route('/sb_invoice_print_check/sb_invoice_print_check/objects/<model("sb_invoice_print_check.sb_invoice_print_check"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sb_invoice_print_check.object', {
#             'object': obj
#         })
