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
	'depends': ['base', 'sale'],
    'data': [
        #SECURITY
        'security/motorcycle_financing_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        #VIEWS
        'views/loan_application_views.xml',
        'views/loan_application_document_views.xml',
        'views/loan_application_document_type_views.xml',
        'views/loan_application_tag_views.xml'
        #MENUS
        'views/motorcycle_financing_menu.xml',
        'views/loan_application_menus.xml'
	],
	'demo': [
        'data/loan_demo.xml',
          ],
	
	'application': True,
    'installable': True,
}