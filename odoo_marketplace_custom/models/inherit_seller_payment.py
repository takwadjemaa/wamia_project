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


from odoo import models, fields, api,exceptions, _
from odoo.exceptions import except_orm, ValidationError, AccessError
import datetime

import logging
_logger = logging.getLogger(__name__)


class SellerPayment(models.Model):
    _inherit = 'seller.payment'
    applied_commission = fields.Float("Marketplace Commission", compute="_get_commission", store=True)
    amount_total = fields.Float("Total Amount", compute="_get_commission", store=True)
    cashable_amountt = fields.Float("Cashable Amount")
    rest_amount = fields.Float("Rest Amount")
    order_state = fields.Selection([("paid", "Paid"), ("pending", "Pending")], default="pending",
                             copy=False, tracking=True)
    # invoice_line_ids2 = fields.Many2many("account.move.line", "seller_paymnet_invoice_line", "seller_payment", "account_invoice_line", "Invoice Lines", readonly="1")
    payment_line_ids = fields.Many2many("seller.payment.line", "seller_paymnet_payment_line", "seller_payment", "seller_payment_line", "payment Lines", readonly="1")





    # @api.depends('seller_id')
    # def _get_cashable_amount(self):
    #
    #     for rec in self:
    #         seller_obj = self.env["res.partner"].browse(rec.seller_id.id)
    #         print(seller_obj)
    #         rec.cashable_amountt = rec.seller_id.cashable_amount
    #         rec.rest_amount = rec.cashable_amountt - rec.amount_total



    @api.depends('invoice_line_ids')
    def _get_commission(self):
        for rec in self:
            rec.applied_commission = 0
            rec.amount_total = 0
            for invoice_line in rec.invoice_line_ids:
                print("invoice_line", invoice_line)
                for invoice in invoice_line:
                    print("invoice", invoice)
                    rec.applied_commission += invoice.seller_commission
                    rec.amount_total += invoice.price_total

    def do_Confirm(self):
        list_ids= []
        for rec in self:
            resConfig = self.env['res.config.settings']
            if rec.payment_type == "dr":
                invoice_type = "in_invoice"
                seller_journal_id = resConfig.get_mp_global_field_value("seller_payment_journal_id")
                if seller_journal_id:
                    journal_ids = self.env['account.journal'].browse([seller_journal_id])
                else:
                    journal_ids = self.env['account.journal'].search(
                        [('type', '=', 'purchase'), ('company_id', '=', rec.seller_id.company_id.id)], limit=1)
            else:
                invoice_type = "out_invoice"
                journal_ids = self.env['account.journal'].search(
                    [('type', '=', 'sale'), ('company_id', '=', rec.seller_id.company_id.id)], limit=1)

            product_id = resConfig.get_mp_global_field_value("seller_payment_product_id")
            rec.cashable_amountt = rec.seller_id.cashable_amount
            rec.rest_amount = rec.cashable_amountt + rec.payable_amount
            # print("----------", rec.cashable_amountt)
            # print("-----rec.invoiced_amount-----", rec.payable_amount)
            # seller invoice line
            for ids_payment_line in rec.payment_line_ids:
                list_ids.append(ids_payment_line.id_payment)
                payment_line = self.env["seller.payment"].search(
                    [('seller_id', '=', rec.seller_id.id)
                        , ('id', 'in',list_ids)])

            print("payment_line------------", payment_line)

            invoice_line_vals = {
                "name": _("Seller Payment"),
                "product_id": product_id,
                # "account_id": rec.seller_id.property_account_payable_id.id,
                "quantity": 1,
                "price_unit": abs(rec.payable_amount),
                "currency_id": rec.currency_id.id,
            }
            default_term = self.env.ref('account.account_payment_term_immediate').id
            invoice_vals = {
                "move_type": "in_invoice",
                "partner_id": rec.seller_id.id,
                "journal_id": journal_ids[0].id if journal_ids else False,
                "invoice_origin": rec.name,
                "currency_id": rec.currency_id.id,
                "invoice_date": rec.date,
                "mp_seller_bill": True,
                "invoice_payment_term_id": default_term,
                "invoice_line_ids": [(0, 0, invoice_line_vals)],
            }
            created_invoice_obj = self.env["account.move"].sudo().with_context(default_type='in_invoice',
                                                                               default_display_name='Seller Bill',
                                                                               default_invoice_payment_term_id=default_term).create(
                invoice_vals)
            if created_invoice_obj:
                created_invoice_obj.seller_payment_ids1 = payment_line
                seller_pay = created_invoice_obj.seller_payment_ids1


                rec.write({
                    "invoice_line_ids": [(6, 0, created_invoice_obj.invoice_line_ids.ids)],
                    "invoice_id": created_invoice_obj.id,
                    "invoiced_amount": created_invoice_obj.amount_total,
                    "state": "posted",
                })

    @api.model
    def seller_action_create_invoice(self):
        amount = 0
        task_list = []
        seller = self[0].seller_id
        resConfig = self.env['res.config.settings']
        for seller_payment in self:


            if seller_payment.state != 'confirm' or seller_payment.seller_id.id != seller.id or seller_payment.order_state != 'pending':
                raise exceptions.UserError(
                    _("You can only create an invoice for a particular seller"))
            else:
                seller_payment.order_state = 'paid'
                amount = amount + seller_payment.payable_amount
                print('ammm', amount)
                invoice_line = seller_payment
                # print("invoice_line",invoice_line)
                # self.invoice_line_ids.seller_payment_ids2 = invoice_line
                # print(" seller_payment.invoice_line_ids------------****", seller_payment.invoice_line_ids)




                # ---------------yessss-------------------------
                task_list.append((0, 0, {'name' :seller_payment.name,'id_payment':seller_payment.id}))

                print('task_list', str(task_list))
                payment_method = self.env["seller.payment.method"].search(
                    [('id', '=', 1)])

                vals = {
                    # "date": seller_payment.date,
                    "seller_id": seller.id,
                    "payment_method": seller.payment_method.ids[0],
                                      #or self.seller_id.payment_method.ids[
                    #     0] if self.seller_id.payment_method else False,
                    "payment_mode": "seller_payment",
                    "description": _("Seller requested for payment..."),
                    "payment_type": "dr",
                    "state": "requested",
                    "memo": seller_payment.memo,
                    "payable_amount": amount,
                    # "payment_line_ids":  [(0, 0,{ 'product_id':''},{'seller_payment_ids2': self } )],
                    "payment_line_ids": task_list,

                }
                # ---------------yessss-------------------------
                # task_list.append((0, 0, {'seller_payment_ids2': seller_payment}))
                #
                # print('task_list', str(task_list))
                #
                # vals = {
                #     # "date": seller_payment.date,
                #     "seller_id": seller.id,
                #     # "payment_method": self.payment_method_id.id or self.seller_id.payment_method.ids[
                #     #     0] if self.seller_id.payment_method else False,
                #     "payment_mode": "seller_payment",
                #     "description": _("Seller requested for payment..."),
                #     "payment_type": "dr",
                #     "state": "requested",
                #     "memo": seller_payment.memo,
                #     "payable_amount": amount,
                #     # "payment_line_ids":  [(0, 0,{ 'product_id':''},{'seller_payment_ids2': self } )],
                #     "payment_line_ids": task_list,
                #
                # }






    # for i in range(0,len(task_list)):
                #     # payment[i]= self.search([("id", "=", task_list[i])])
                #     print('payment------------------>',task_list[i])
                #     seller_payment_vals[i] = {'name': task_list[i].name}
                #     print("seller_payment_vals[i]",seller_payment_vals[i])







                # self.payment_line_ids.seller_payment_ids2 = seller_payment_vals
                # print("payment_line_ids------------****", self.payment_line_ids)
                # print('seller_payment_vals',seller_payment_vals)
                #
                # invoice_line_vals = {
                #
                #     "seller_payment_ids2": seller_payment_vals,
                # }
                #
                # print("task_list",task_list)
                # print("seller_payment_ids2",seller_payment.invoice_line_ids2.seller_payment_ids2.name)
                # print("invoice_line_ids2",seller_payment.invoice_line_ids2)
                # for invo in seller_payment.invoice_line_ids2:
                #     # invo.seller_payment_ids2.name = self.name
                #     print(" invo.seller_payment_ids2.name", invo.seller_payment_ids2.name)




        print("vals---------",vals)
        #
        # # invo = self.invoice_line_ids2.seller_payment_ids2
        # print("seller_payment.invoice_line_ids2.seller_payment_ids1---------", self.invoice_line_ids2.seller_payment_ids2)

        #
        # seller_payment_vals = {
        #     "seller_id": seller,
        #     "payment_mode": 'seller_payment',
        #     "payable_amount": amount,
        #
        # }

        self.create(vals)

class SellerPaymentLine(models.Model):
    _name = 'seller.payment.line'
    _inherit = ['mail.thread']
    _description = "Seller Payment line"

    name = fields.Char(string="Record Reference",
                       default="NEW")
    # seller_payment_ids2 = fields.One2many('seller.payment','payment_line_ids', string='Seller Payment line', ondelete='restrict' )
    product_id = fields.Many2one('product.product', string='Product', ondelete='restrict')
    id_payment = fields.Integer( store=True)




