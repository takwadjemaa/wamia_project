# -*- coding: utf-8 -*-
# from odoo import http


# class HrAttendanceTakwa(http.Controller):
#     @http.route('/hr_attendance_takwa/hr_attendance_takwa', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_attendance_takwa/hr_attendance_takwa/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_attendance_takwa.listing', {
#             'root': '/hr_attendance_takwa/hr_attendance_takwa',
#             'objects': http.request.env['hr_attendance_takwa.hr_attendance_takwa'].search([]),
#         })

#     @http.route('/hr_attendance_takwa/hr_attendance_takwa/objects/<model("hr_attendance_takwa.hr_attendance_takwa"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_attendance_takwa.object', {
#             'object': obj
#         })
