# -*- coding: utf-8 -*-
# from odoo import http


# class ChangesAnsacero(http.Controller):
#     @http.route('/changes_ansacero/changes_ansacero', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/changes_ansacero/changes_ansacero/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('changes_ansacero.listing', {
#             'root': '/changes_ansacero/changes_ansacero',
#             'objects': http.request.env['changes_ansacero.changes_ansacero'].search([]),
#         })

#     @http.route('/changes_ansacero/changes_ansacero/objects/<model("changes_ansacero.changes_ansacero"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('changes_ansacero.object', {
#             'object': obj
#         })
