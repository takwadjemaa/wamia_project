# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    shop_categories = fields.Many2one(
        'shop.category', string='Shop Category', ondelete='restrict', copy=False)
