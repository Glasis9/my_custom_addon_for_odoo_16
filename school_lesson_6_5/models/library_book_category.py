from odoo import models, _


class LibraryBookCategory(models.Model):
    """
    Inherit the "library.book.category" class from the school_lesson_6_1
    module and extend it with an additional method
    """

    _inherit = "library.book.category"

    def action_view_trie_all_book_category(self):
        """
        Button that displays a tree with books
        belonging to this current category
        """

        self.ensure_one()
        return {
            "name": _("View all book this category"),
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "library.book",
            "target": "new",
            "domain": [("category_id", "=", self.id)],
        }
