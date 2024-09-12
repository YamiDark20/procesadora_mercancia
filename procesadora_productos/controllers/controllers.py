# -*- coding: utf-8 -*-
# from odoo import http


# class ProcesadoraProductos(http.Controller):
#     @http.route('/procesadora_productos/procesadora_productos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/procesadora_productos/procesadora_productos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('procesadora_productos.listing', {
#             'root': '/procesadora_productos/procesadora_productos',
#             'objects': http.request.env['procesadora_productos.procesadora_productos'].search([]),
#         })

#     @http.route('/procesadora_productos/procesadora_productos/objects/<model("procesadora_productos.procesadora_productos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('procesadora_productos.object', {
#             'object': obj
#         })
