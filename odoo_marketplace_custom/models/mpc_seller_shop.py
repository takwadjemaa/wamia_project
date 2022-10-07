from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class SellerShopCustom(models.Model):
    _inherit = 'seller.shop'

    shop_tag_line = fields.Many2one(related="seller_id.shop_categories", string="Shop Category")