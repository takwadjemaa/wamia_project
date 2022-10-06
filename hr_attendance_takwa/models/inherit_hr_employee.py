

from odoo import models, fields, api, exceptions, _
from odoo.tools import float_round
from odoo.exceptions import  ValidationError

from odoo.http import request


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def attendance_manual(self, next_action, entered_pin=None):
        self.ensure_one()
        # print("this action")
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        # print("ip_address", ip_address)
        user_rec = request.env['res.users'].sudo().search([("id", "=", self.user_id.id)], limit=1)
        # print(user_rec)
        # print("user_rec.allowed_ips", user_rec.allowed_ips)
        if user_rec.allowed_ips:
            ip_list = []
            for rec in user_rec.allowed_ips:
                ip_list.append(rec.ip_address)
            if ip_address in ip_list:
                # print("yes")
                return super(HrEmployee,self).attendance_manual(next_action)
            else:
                raise exceptions.ValidationError(_('Not allowed from this IP'))
                # print("no")
                # raise exceptions.ValidationError(_('Not allowed from this IP'))
                # raise exceptions.ValidationError("Not allowed from this IP")
                # print("no")
                # return {'warning': _('Not allowed from this IP')}
                # raise Warning("Not allowed from this IP")
