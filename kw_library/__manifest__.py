{
    "name": "kw_library",

    "license": "Other proprietary",

    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    "author": "My Company",

    "website": "http://www.yourcompany.com",

    "category": "Uncategorized",

    "version": "16.0.1.0.0",

    # any module necessary for this one to work correctly
    "depends": ["base"],

    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/book.xml",
        "views/author.xml"
    ],

    # only loaded in demonstration mode
    # "demo": [
    #     "demo/demo.xml",
    # ],
}