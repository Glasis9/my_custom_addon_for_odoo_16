from odoo import models, fields


class HospitalVisitsPatient(models.Model):
    _name = "hospital.visits.patient"
    _description = "Hospital Visits Patient"
    _rec_name = "date_visit"

    name_patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="Name patient",
        ondelete="cascade",
    )
    observing_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Observing doctor",
        ondelete="cascade",
    )
    diagnosis_ids = fields.Many2many(
        comodel_name="hospital.diagnosis",
        string="Diagnosis",
    )
    date_visit = fields.Datetime(
        string="Date visit",
        default=fields.date.today(),
        help="The date when the patient came to the doctor",
    )
