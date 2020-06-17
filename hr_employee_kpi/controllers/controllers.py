# -*- coding: utf-8 -*-
from odoo import http

# class EmployeeKpi(http.Controller):
#     @http.route('/employee_kpi/employee_kpi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_kpi/employee_kpi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_kpi.listing', {
#             'root': '/employee_kpi/employee_kpi',
#             'objects': http.request.env['employee_kpi.employee_kpi'].search([]),
#         })

#     @http.route('/employee_kpi/employee_kpi/objects/<model("employee_kpi.employee_kpi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_kpi.object', {
#             'object': obj
#         })