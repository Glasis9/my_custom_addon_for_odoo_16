from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LibraryBookCategory(models.Model):
    _name = "library.book.category"
    _description = "Library Book Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    name = fields.Char(index="trigram", required=True)
    complete_name = fields.Char(
        compute="_compute_complete_name", recursive=True, store=True
    )
    parent_id = fields.Many2one(
        comodel_name="library.book.category",
        index=True,
        ondelete="cascade",
    )
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many(
        comodel_name="library.book.category", inverse_name="parent_id"
    )
    book_count = fields.Integer(
        compute="_compute_book_count",
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = "%s / %s" % (
                    category.parent_id.complete_name,
                    category.name,
                )
            else:
                category.complete_name = category.name

    def _compute_book_count(self):
        for obj in self:
            obj.book_count = self.env["library.book"].search_count([
                ("category_id", "child_of", obj.id)
            ])

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))
