# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
{
  "name"                 :  "Module For Merging Pos/Website Coupons",
  "summary"              :  "The module is used to merge two modules together namely, Odoo POS coupons and Odoo Website Coupons & Vouchers",
  "category"             :  "Website",
  "version"              :  "5.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo.html",
  "description"          :  """POS coupons & Vouchers
Odoo POS coupons
POS vouchers
Voucher code
Coupon code
Manage vouchers
Discount coupons
Discount vouchers
Sale vouchers
Coupons & vouchers
POS discount sale
coupon discount
Odoo Website Coupons & Vouchers
Website coupons
Website vouchers
Voucher code
Coupon code
Manage vouchers
Discount coupons
Discount vouchers
Sale vouchers
Coupons & vouchers""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=wk_coupons",
  "depends"              :  [
                             'sale',
                             'mail',
                            ],
  "data"                 :  [
                             'views/wk_coupon_view.xml',
                             'views/coupon_history_view.xml',
                             'report/report.xml',
                             'report/report_template.xml',
                             'security/ir.model.access.csv',
                             'data/coupon_data_view.xml',
                             'data/mail_template.xml',
                             'views/res_config_view.xml',
                             'wizard/wizard_view.xml',
                            ],
  "demo"                 :  ['data/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  1,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}