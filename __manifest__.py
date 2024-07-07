# -*- coding: utf-8 -*-
{
    'name': "test_app",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Mohammed",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board', 'hr', 'mail'],

    # always loaded
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        # 'wizards/session_search_view.xml',
        'wizards/change_course_state_view.xml',
        'views/views.xml',
        'views/session_board.xml',
        'views/employee_view.xml',
        'views/course_history_view.xml',

        # 'reports/orders_report.xml',
        # 'reports/extract_report.xml',

        # 'reports/test_app_reports.xml',
        # 'reports/test_app_templates.xml',
        'reports/session_report.xml',
        'views/course_view.xml',
        # 'reports/extract_report.xml',
        # 'views/partner.xml',
        # 'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': ['test_app/static/src/css/property.css']
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
