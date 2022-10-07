# -*- coding: utf-8 -*-
{
    'name': "odoo_marketplace_custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Marketplace',
    'version': '0.1',
    'sequence': 10,

    # any module necessary for this one to work correctly
    'depends': ['base', 'odoo_marketplace', 'stock', 'sale', 'marketplace_seller_wise_checkout', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/custom_stock_report_view.xml',
        'views/category_shop_view.xml',
        'views/stock_picking.xml',
        'views/website_mpc_template.xml',
        'views/mpc_seller_view.xml',
        'views/inherit_seller_payment_view.xml',
        'views/seller_payment_action.xml',
        'report/seller_payment_report.xml',
        'views/inherit_account_invoice_view.xml',
        'report/acount_repot.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
