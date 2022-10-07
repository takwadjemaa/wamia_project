from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    @api.model
    def get_mp_ajax_shop_category(self):
        shop_categories = self.env['shop.category'].sudo().search([])
        return shop_categories
