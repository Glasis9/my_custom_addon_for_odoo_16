import datetime

from odoo import models, fields, api


class HospitalAnalysis(models.Model):
    _name = "hospital.analysis"
    _description = "Analysis"
    _rec_name = "analysis"

    types_analysis_ids = fields.Many2many(
        string="Types analysis",
        comodel_name="hospital.types.analysis",
    )

    name_patient_id = fields.Many2one(
        required=True,
        comodel_name="hospital.patient",
        string="Patient",
        ondelete="cascade",
    )
    date = fields.Date(required=True, default=datetime.date.today())
    analysis = fields.Char(compute="_compute_name", readonly=True, store=True)
    price = fields.Integer(compute="_compute_price", readonly=True, store=True)

    # def name_get(self):
    #     return [
    #         (obj.id, "%s, %s" % (
    #             obj.analysis, f"types: {', '.join(
    #     [type.name for type in obj.types_analysis_ids]
    #     )}"
    #         )
    #          ) for obj in self]

    @api.depends("types_analysis_ids")
    def _compute_name(self):
        for obj in self:
            obj.analysis = ", ".join(
                [type.name for type in obj.types_analysis_ids]
            )

    @api.depends("types_analysis_ids")
    def _compute_price(self):
        for obj in self:
            obj.price = sum([type.price for type in obj.types_analysis_ids])
