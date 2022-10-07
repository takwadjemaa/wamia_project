# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class odoo_marketplace_custom(models.Model):
#     _name = 'odoo_marketplace_custom.odoo_marketplace_custom'
#     _description = 'odoo_marketplace_custom.odoo_marketplace_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state_id = fields.Many2one(related="partner_id.state_id", string="Delivery Address", store="True")


class SaleOrder(models.Model):
    _inherit = "sale.order"



