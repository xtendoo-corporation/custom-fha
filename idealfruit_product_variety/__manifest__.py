# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Ideal Fruit product variety",
    "version": "16.0.1.0.1",
    "development_status": "Beta",
    "category": "Product",
    "summary": "Ideal Fruit product variety",
    "author": "Dani Domínguez (Xtendoo), ",
    "website": "https://github.com/xtendoo-corporation/",
    "license": "AGPL-3",
    "depends": [
        "product",
        "purchase",
        "account",
        "stock",
    ],
    "data": [
        "views/purchase_order_line_views.xml",
        "views/product_variety_views.xml",
        "views/account_move_line_views.xml",
        "views/product_category_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
