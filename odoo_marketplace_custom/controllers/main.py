# -*- coding: utf-8 -*-
# from odoo import http
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import WebsiteSale, QueryURL, TableCompute

PPG = 20  # Products Per Page
PPR = 4   # Products Per Row

SPG = 20  # Shops/sellers Per Page
SPR = 4   # Shops/sellers Per Row

class ShopsHyperlocal(http.Controller):



    @http.route([
        '/shop_category',

    ], type='http', auth="public", website=True)
    def load_shop(self, page=0, search='', ppg=False, **post):
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        PPR = request.env['website'].get_current_website().shop_ppr or 4

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = SPG
            post["ppg"] = ppg
        else:
            ppg = SPG

        domain = []
        keep = QueryURL('/shop_category', search=search)

        url = "/shop_category"
        if search:
            post["search"] = search

        shop_obj = request.env['shop.category'].sudo().search([])
        seller_shop_count = shop_obj.sudo().search_count(domain)
        pager = request.website.pager(url=url, total=seller_shop_count, page=page, step=ppg, scope=7, url_args=post)
        categ_shops = shop_obj.sudo().search(domain, limit=ppg, offset=pager['offset'])
        print(shop_obj)


        values = {
            'search': search,
            'pager': pager,
            'categ_shops': shop_obj,
            'search_count': seller_shop_count,  # common for all searchbox
            # 'bins': TableCompute().process(categ_shops, ppg, PPR),
            'ppg': ppg,
            'ppr': PPR,
            'rows': SPR,
            'keep': keep,
        }
        return request.render("odoo_marketplace_custom.category_shop_list", values)

    #
    # @http.route([
    #     '/',
    #
    # ], type='http', auth="public", website=True)
    # def load_category(self):
    #     # if not ppg:
    #     #     ppg = request.env['website'].get_current_website().shop_ppg
    #     #
    #     # PPR = request.env['website'].get_current_website().shop_ppr
    #     # if ppg:
    #     #     try:
    #     #         ppg = int(ppg)
    #     #     except ValueError:
    #     #         ppg = SPG
    #     #     post["ppg"] = ppg
    #     # else:
    #     #     ppg = SPG
    #
    #     # domain = self._get_seller_search_domain(search)
    #     # keep = QueryURL('/', search=search)
    #     #
    #     # url = "/"
    #     # if search:
    #     #     post["search"] = search
    #
    #     shop_obj = request.env['shop.category'].sudo().search([])
    #     # shop_count = shop_obj.sudo().search_count(domain)
    #     # total_active_seller = shop_obj.sudo().search_count(self._get_seller_search_domain(""))
    #     # pager = request.website.pager(url=url, total=shop_count, page=page, step=ppg, scope=7, url_args=post)
    #     # shop_objs = shop_obj.sudo().search(domain, limit=ppg, offset=pager['offset'],
    #     #                                        order=self._get_search_order(post))
    #
    #     # shop_timing = request.env['store.timing'].sudo().search([])
    #
    #     values = {
    #         # 'search': search,
    #         # 'pager': pager,
    #         'shop_obj': shop_obj,
    #         # 'search_count': shop_count,  # common for all searchbox
    #         # 'bins': TableCompute().process(shop_objs, ppg, PPR),
    #         # 'ppg': ppg,
    #         # 'ppr': PPR,
    #         # 'rows': SPR,
    #         # 'keep': keep,
    #         # 'total_active_seller': total_active_seller,
    #         # 'shop_timing': shop_timing,
    #     }
    #     return request.render("odoo_marketplace_custom.category_shop_list", values)


class WebsiteSale(WebsiteSale):
    @http.route([
        '''/shopss''',
        '''/shopss/page/<int:page>''',
        '''/shopss/category/<model("shop.category"):category>''',
        '''/shopss/category/<model("shop.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=False)
    def shop_catt(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        try:
            min_price = float(min_price)
        except ValueError:
            min_price = 0
        try:
            max_price = float(max_price)
        except ValueError:
            max_price = 0
        Category = request.env['shop.category']
        if category:
            category = Category.search([], limit=1)
            if not category:
                raise NotFound()
        else:
            category = Category

        # Category = request.env['shop.category']
        # if category:
        #     category = Category.search([('id', '=', int(category))], limit=1)
        #     if not category or not category.can_access_from_current_website():
        #         raise NotFound()
        # else:
        #     category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shopss', category=category and int(category), search=search, attrib=attrib_list,
                        min_price=min_price, max_price=max_price, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            company_currency = request.website.company_id.currency_id
            conversion_rate = request.env['res.currency']._get_conversion_rate(company_currency, pricelist.currency_id,
                                                                               request.website.company_id,
                                                                               fields.Date.today())
        else:
            conversion_rate = 1

        url = "/shopss"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        options = self._get_search_options(
            category=category,
            attrib_values=attrib_values,
            pricelist=pricelist,
            min_price=min_price,
            max_price=max_price,
            conversion_rate=conversion_rate,
            **post
        )
        # No limit because attributes are obtained from complete product list
        shop_count, details, fuzzy_search_term = request.website._search_with_fuzzy("products_only", search,
                                                                                       limit=None,
                                                                                       order=self._get_search_order(
                                                                                           post), options=options)
        search_shop = request.env['seller.shop'].sudo().search(
                               []).with_context(bin_size=True)
        shop_count = len(search_shop)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            # TODO Find an alternative way to obtain the domain through the search metadata.
            Product = request.env['product.template'].with_context(bin_size=True)
            domain = self._get_search_domain(search, category, attrib_values)

            # This is ~4 times more efficient than a search for the cheapest and most expensive products
            from_clause, where_clause, where_params = Product._where_calc(domain).get_sql()
            query = f"""
                   SELECT COALESCE(MIN(list_price), 0) * {conversion_rate}, COALESCE(MAX(list_price), 0) * {conversion_rate}
                     FROM {from_clause}
                    WHERE {where_clause}
               """
            request.env.cr.execute(query, where_params)
            available_min_price, available_max_price = request.env.cr.fetchone()

            if min_price or max_price:
                # The if/else condition in the min_price / max_price value assignment
                # tackles the case where we switch to a list of products with different
                # available min / max prices than the ones set in the previous page.
                # In order to have logical results and not yield empty product lists, the
                # price filter is set to their respective available prices when the specified
                # min exceeds the max, and / or the specified max is lower than the available min.
                if min_price:
                    min_price = min_price if min_price <= available_max_price else available_min_price
                    post['min_price'] = min_price
                if max_price:
                    max_price = max_price if max_price >= available_min_price else available_max_price
                    post['max_price'] = max_price

        website_domain = request.website.website_domain()
        categs_domain =  website_domain
        if search:
            search_categories = Category.search(
                [] + website_domain).parents_and_self
            # categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        pager = request.website.pager(url=url, total=shop_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        shop = search_shop[offset:offset + ppg]


        values = {
            'search': fuzzy_search_term or search,
            'original_search': fuzzy_search_term and search,
            'category': category,

            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'shops': search_shop,
            'search_count': shop_count,  # common for all searchbox
            'bins': TableCompute().process(shop, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'keep': keep,
            'search_categories_ids': search_categories.ids,

        }

        if category:
            values['main_object'] = category
        return request.render("odoo_marketplace_custom.shop_category", values)
    #
    # @http.route([
    #
    #     '''/shopss''',
    #     '''/shopss/page/<int:page>''',
    #     '''/shopss/category/<model("shop.category"):category>''',
    #     '''/shopss/category/<model("shop.category"):category>/page/<int:page>'''
    # ], type='http', auth="public", website=True, sitemap=WebsiteSale().sitemap_shop)
    # def category_shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
    #     location = False
    #     latitude = False
    #     longitude = False
    #     # res = super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)
    #     enable_hyperlocal = request.website.enable_hyperlocal
    #     if enable_hyperlocal:
    #         add_qty = int(post.get('add_qty', 1))
    #         try:
    #             min_price = float(min_price)
    #         except ValueError:
    #             min_price = 0
    #         try:
    #             max_price = float(max_price)
    #         except ValueError:
    #             max_price = 0
    #
    #         Category = request.env['shop.category']
    #         if category:
    #             category = Category.search([], limit=1)
    #             if not category:
    #                 raise NotFound()
    #         else:
    #             category = Category
    #
    #         if ppg:
    #             try:
    #                 ppg = int(ppg)
    #                 post['ppg'] = ppg
    #             except ValueError:
    #                 ppg = False
    #         if not ppg:
    #             ppg = request.env['website'].get_current_website().shop_ppg or 20
    #
    #         ppr = request.env['website'].get_current_website().shop_ppr or 4
    #
    #         attrib_list = request.httprequest.args.getlist('attrib')
    #         attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
    #         attributes_ids = {v[0] for v in attrib_values}
    #         attrib_set = {v[1] for v in attrib_values}
    #
    #         keep = QueryURL('/shopss', category=category and int(category), search=search, attrib=attrib_list,
    #                         min_price=min_price, max_price=max_price, order=post.get('order'))
    #
    #         pricelist_context, pricelist = self._get_pricelist_context()
    #
    #         request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
    #
    #         filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
    #         if filter_by_price_enabled:
    #             company_currency = request.website.company_id.currency_id
    #             conversion_rate = request.env['res.currency']._get_conversion_rate(company_currency,
    #                                                                                pricelist.currency_id,
    #                                                                                request.website.company_id,
    #                                                                                fields.Date.today())
    #         else:
    #             conversion_rate = 1
    #
    #         url = "/shop"
    #         if search:
    #             post["search"] = search
    #         if attrib_list:
    #             post['attrib'] = attrib_list
    #
    #         options = {
    #             'displayDescription': True,
    #             'displayDetail': True,
    #             'displayExtraDetail': True,
    #             'displayExtraLink': True,
    #             'displayImage': True,
    #             'allowFuzzy': not post.get('noFuzzy'),
    #             'category': str(category.id) if category else None,
    #             'min_price': min_price / conversion_rate,
    #             'max_price': max_price / conversion_rate,
    #             'attrib_values': attrib_values,
    #             'display_currency': pricelist.currency_id,
    #         }
    #         # No limit because attributes are obtained from complete product list
    #
    #         shop_count, details, fuzzy_search_term = request.website._search_with_fuzzy("products_only", search,
    #                                                                                     limit=None,
    #                                                                                     order=self._get_search_order(
    #                                                                                         post), options=options)
    #
    #         search_shop = details[0].get('results', request.env['seller.shop']).with_context(bin_size=True)
    #         latLong = request.env['seller.ship.rate'].sudo().getdefaultLongLat()
    #         if latLong:
    #             sellerShipAreaObjs = request.env['seller.ship.area'].sudo().search([])
    #             sellerIds = self.getAvailableSellers(sellerShipAreaObjs, latLong)
    #             if sellerIds:
    #                 search_shop = request.env['seller.shop'].sudo().search(
    #                     [('seller_id', 'in', sellerIds)]).with_context(bin_size=True)
    #                 shop_count = len(search_shop)
    #
    #
    #             else:
    #                 search_shop = request.env['seller.shop']
    #                 shop_count = len(search_shop)
    #
    #
    #         website_domain = request.website.website_domain()
    #         categs_domain =  website_domain
    #         if search:
    #             print("ccccccccccccc")
    #             search_categories = Category.search(
    #                 [('id', 'in', search_shop.shop_tag_line)] + website_domain).parents_and_self
    #             print("search_categories",search_categories)
    #             categs_domain.append(('id', 'in', search_categories.ids))
    #         else:
    #             search_categories = Category
    #         categs = Category.search(categs_domain)
    #
    #         if category:
    #             url = "/shopss/category/%s" % slug(category)
    #
    #         pager = request.website.pager(url=url, total=shop_count, page=page, step=ppg, scope=7, url_args=post)
    #         offset = pager['offset']
    #         shop = search_shop[offset:offset + ppg]
    #
    #         values = {
    #             'search': fuzzy_search_term or search,
    #             'original_search': fuzzy_search_term and search,
    #             'category': category,
    #             'attrib_values': attrib_values,
    #             'attrib_set': attrib_set,
    #             'pager': pager,
    #             'pricelist': pricelist,
    #             'add_qty': add_qty,
    #             'products': shop,
    #             'search_count': shop_count,  # common for all searchbox
    #             'bins': TableCompute().process(shop, ppg, ppr),
    #             'ppg': ppg,
    #             'ppr': ppr,
    #             'categories': categs,
    #             'keep': keep,
    #             'search_categories_ids': search_categories.ids,
    #         }
    #         if category:
    #             values['main_object'] = category
    #         return request.render("odoo_marketplace_custom.shop_category", values)






