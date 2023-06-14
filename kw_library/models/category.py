import logging

from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class BookCategory(models.Model):
    _name = "kw.lib.book.category"
    _description = "Book Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    name = fields.Char("Name", index="trigram", required=True)
    complete_name = fields.Char(
        "Complete Name", compute="_compute_complete_name", recursive=True, store=True
    )
    parent_id = fields.Many2one(
        "kw.lib.book.category", "Parent Category", index=True, ondelete="cascade"
    )
    parent_path = fields.Char(index=True)
    child_id = fields.One2many(
        comodel_name="kw.lib.book.category",
        inverse_name="parent_id",
        string="Child Categories"
    )
    book_count = fields.Integer(
        compute="_compute_book_count",
        help="The number of book under this category "
        "(Does not consider the children categories)",
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
            obj.product_count = self.env["kw.lib.book"].search_count([
                ("category_id", "child_of", obj.id)
            ])

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))
