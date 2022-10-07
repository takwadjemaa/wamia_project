# -*- coding: utf-8 -*-
# from odoo import http


# class OdooMarketplaceCustom(http.Controller):
#     @http.route('/odoo_marketplace_custom/odoo_marketplace_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_marketplace_custom/odoo_marketplace_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_marketplace_custom.listing', {
#             'root': '/odoo_marketplace_custom/odoo_marketplace_custom',
#             'objects': http.request.env['odoo_marketplace_custom.odoo_marketplace_custom'].search([]),
#         })

#     @http.route('/odoo_marketplace_custom/odoo_marketplace_custom/objects/<model("odoo_marketplace_custom.odoo_marketplace_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_marketplace_custom.object', {
#             'object': obj
#         })
