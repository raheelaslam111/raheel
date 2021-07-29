##############################################################################
{
    'name': 'Sale Purchase Discount in Lines',
    'version': '14.0',
    'author': 'Mian Furqan Amjad',
    'company': 'Mian Furqan Amjad',
    'website': 'https://www.abc.com',
    'category': 'hidden',
    'license': 'AGPL-3',
    'sequence': 15,
    'summary': 'customization in Sale purchase',
    'images': [],
    'depends': ['sale','purchase'],
    'description': """Furqan.amjad123@gmail.com, Data Scientest and Team Lead, Project Manager
========================================================================
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/sale_purchase.xml',
        'views/purchase.xml',
        # 'views/account_report_with_payment.xml',
        # 'views/invoice_inherit.xml',
    ],
    # 'qweb': [
    #     "static/src/xml/reset_to_draft.xml",
    # ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
