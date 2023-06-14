{
    "name": "kw_library",
    "license": "Other proprietary",
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    "category": "Uncategorized",
    "version": "16.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base"],

    # Добавляем внешние библиотеки
    "external_dependencies": {"python": ["pyisbn", ], },
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/book.xml",
        "views/author.xml",
        "views/category.xml",
        "views/book_instance.xml",
        "data/ir_sequence.xml",
    ],
}
