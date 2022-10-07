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
  "name"                 :  "Website Loyalty Program",
  "summary"              :  "Run loyalty rewards program in your store. The customer can earn loyalty points on purchases and redeem those points on subsequent purchases.",
  "category"             :  "Website",
  "version"              :  "2.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Website-Loyalty-Management.html",
  "description"          :  """Odoo Website Loyalty Management
Odoo website Rewards Program
Odoo Loyalty points website
rewards program
website  coupons 
website vouchers
Discount vouchers
customer loyalty program
Purchase points
Redeem points
Rewards point
loyalty wallet
Website loyalty programme
website members loyalty
Loyalty member points""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_loyalty_management",
  "depends"              :  [
                             'website_virtual_product',
                             'wk_wizard_messages',
                             'portal',
                             'website_sale_management',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/res_config_view.xml',
                             'views/template.xml',
                             'views/website_loyalty_management.xml',
                             'data/data.xml',
                            ],
  "assets"              :  {
    "web.assets_frontend" : [
      'website_loyalty_management/static/src/js/website_loyalty_management.js',
      'website_loyalty_management/static/src/css/website_loyalty_management.css'
    ]
  },
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}