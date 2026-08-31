# Manifest Template. If you copy this template, make sure the indentation is right.
{
	'name': 'Motorcycle Financing',
    'summary': 'Streamlines the loan application process for dealerships.',
	'description': '',
    'license': 'OPL-1',
	'category': 'Kawiil',
	'author': 'JGJ-GWCG',
	'website': 'https://github.com/JGJ-GWCG/custom_addons.git',
	'version': '19.0.0.0.1',
	'depends': ['base'],
    'data': [
        #SECURITY
        'security/ir.model.access.csv',
        #VIEWS
        'views/loan_application_views.xml',
        #MENUS
        'views/motorcycle_financing_menu.xml'
	],
	'demo': [
        'data/loan_demo.xml',
          ],
	
	'application': True,
    'installable': True,
}