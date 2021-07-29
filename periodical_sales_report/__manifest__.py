# -*- coding: utf-8 -*-

{
    'name' : 'Periodical Sale Report',
    'version' : '13.0.1',
    'summary': 'Module print daily, last week and last month sale report. and with respect to Salesperson',
    'sequence': 16,
    'category': 'Sales',
    'author' : 'Raheel Aslam and Aminia Technology',
    'description': """
Custom Sales Report
=====================================
This module print daily, last week and last month sale report.
Also print report for particular duration.
    """,
    'depends' : ['base_setup', 'sale_management','sale'],
    'data': [
        'wizard/wiz_periodical_report_view.xml',
        'wizard/wiz_periodical_report_view_partner.xml',
        'views/periodical_report.xml',
        'views/report_periodical_sales.xml',
        'views/report_periodical_sales_person.xml',
    ],
    'images': [
        'static/description/raheel.jpg'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
