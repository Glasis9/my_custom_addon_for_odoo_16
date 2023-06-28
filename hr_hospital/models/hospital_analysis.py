from odoo import models, fields


class HospitalAnalysis(models.Model):
    _name = "hospital.analysis"
    _description = "Analysis"
    _rec_name = "name_patient_id"

    name_patient_id = fields.Many2one(
        required=True,
        comodel_name="hospital.patient",
        string="Patient",
        ondelete="cascade",
    )
    analysis = fields.Char()
