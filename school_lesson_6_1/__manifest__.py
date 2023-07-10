# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'School Lesson 6 1',
    'version': '15.0.0.0.2',
    'category': 'Extra Tools',
    'summary': """
        Odoo School
        Lesson 6-1: Master and data data.
    """,
    'license': 'LGPL-3',
    'author': ['Garazd Creation', 'Oleg Usenko'],
    'website': 'https://garazd.biz',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_menus.xml',
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'data/res_partner_data.xml',
        'data/library_book_category_data.xml',
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/res_partner_bank_demo.xml',
        'demo/library_book_demo.xml',
        'demo/library_book_change_demo.xml',
    ],
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
