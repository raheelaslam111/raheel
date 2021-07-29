##############################################################################
{
    'name': 'Petty Cash',
    'version': '14.0',
    'author': 'Raheel Aslam',
    'company': 'Code Ninja',
    'website': 'https://www.codeninja.pk',
    'category': 'hidden',
    'sequence': 15,
    'summary': 'Managing the petty cash of employee/customer',
    'images': [],
    'depends': ['base','sale','purchase','account','project'],
    'description': """Managing the petty cash of employee/customer
========================================================================
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/petty_cash_request.xml',
        'views/petty_cash_holder.xml',
        'data/sequence.xml',
        'views/menus.xml',

    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
