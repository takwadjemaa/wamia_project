# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, fields, api, _
from lxml import etree
from odoo.fields import datetime,date
from datetime import timedelta

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    seller_payment_ids1 = fields.Many2many("seller.payment", "account_move_id", string="Seller Payment")
    seller_commission = fields.Monetary("Marketplace Commission", compute='_get_total', store=True)
    total_amountt = fields.Monetary(string="Total", compute='_get_total', store=True)

    @api.depends('seller_payment_ids1')
    def _get_total(self):
        for rec in self:
            if rec.move_type == "in_invoice":
                # , 'in_refund',  'in_receipt')
                ligns = self.seller_payment_ids1
                for payment in ligns:
                    # print("payment", payment)
                    rec.seller_commission += payment.applied_commission
                    rec.total_amountt = rec.amount_total + rec.seller_commission
                    # print("rec.payable_amountt", rec.seller_commission)
                    # print("rec.seller_commission", rec.total_amountt)

            else:
                rec.total_amountt = 0
                rec.seller_commission = 0


# class AccountInvoiceLine(models.Model):
#     _inherit = "account.move.line"

    # seller_payment_ids2 = fields.Many2one('seller.payment', string='Seller Paymentttt', ondelete='restrict')



