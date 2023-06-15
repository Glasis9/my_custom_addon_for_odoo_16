from odoo import models, fields


class HospitalDiagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "Hospital Diagnosis"
    _rec_name = "diagnosis"

    diagnosis = fields.Char(required=True)
