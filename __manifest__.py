# -*- coding: utf-8 -*-
{
    'name': 'qimamhd_sales_extend_13',
	'version': '13.0.1.0.0',
	'summary': 'qimamhd_sales_extend_13',
	'category': 'Tools',
	'author': 'Developers team',
	'maintainer': 'qimamhd-tech Techno Solutions',
	'company': 'qimamhd-tech Techno Solutions',
	'website': 'https://www.qimamhd-tech.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','qimamhd_sales_forms','custom_branch_13'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/sales_man_branch_view.xml',
	#'wizards/recap.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
