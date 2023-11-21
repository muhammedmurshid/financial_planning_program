{
    'name': "Financial Planning Program",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail', 'logic_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/financial_planning.xml',
        'security/rules.xml'
    ],
    'demo': [],
    'summary': "financial_planning_program",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
