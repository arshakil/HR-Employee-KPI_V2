# -*- coding: utf-8 -*-
{
    'name': "HR Employee KPI",

    'summary': """
    This is module is used to record and monitor periodic KPI for each employee.
    """,

    'description': """
    A performance indicator or key performance indicator (KPI) is a type of Performance measurement. 
    KPIs evaluate the success of an organization or of a particular activity (such as Employee Performance) in which it engages.
    """,

    'author': "Metamorphosis",
    'website': "https://metamorphosis.com.bd",
    'sequence': '1',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '10.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/employee_kpi.xml',
        'views/employee_kpi_assign.xml',
        'views/assets.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'images': ['static/description/cover.png'],
    'icon': "/hr_employee_kpi/static/description/icon.png",
    'installable': True,
    'application': True,
    "license": "OPL-1",
    'price':199.0,
    'currency':'EUR',
}