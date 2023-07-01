from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalTypesAnalysis(models.Model):
    _name = "hospital.types.analysis"
    _description = "Types analysis"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    name = fields.Char(index="trigram", required=True)
    complete_name = fields.Char(
        compute="_compute_complete_name", recursive=True, store=True
    )
    parent_id = fields.Many2one(
        comodel_name="hospital.types.analysis",
        index=True,
        ondelete="cascade",
    )
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many(
        comodel_name="hospital.types.analysis", inverse_name="parent_id"
    )
    analysis_count = fields.Integer(
        compute="_compute_analysis_count",
    )
    price = fields.Integer(string="Price in USD")

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for types in self:
            if types.parent_id:
                types.complete_name = "%s / %s" % (
                    types.parent_id.complete_name,
                    types.name,
                )
            else:
                types.complete_name = types.name

    def _compute_analysis_count(self):
        for obj in self:
            obj.analysis_count = self.env["hospital.analysis"].search_count([
                ("types_analysis_ids", "child_of", obj.id)
            ])

    @api.constrains("parent_id")
    def _check_types_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive types."))
