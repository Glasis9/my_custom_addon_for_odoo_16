from odoo import models, fields


class HospitalHistoryChangingPersonalDoctor(models.Model):
    _name = "hospital.history.changing.personal.doctor"
    _description = "History of changing a personal doctor"
    _rec_name = "name_patient_id"

    choice_doctor_date_time = fields.Datetime()
    name_patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="Patient",
        ondelete="cascade",
    )
    name_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Doctor",
        ondelete="cascade",
    )

    def name_get(self):
        return [(obj.id, f"Patient: {obj.name_patient_id.name}, "
                         f"Doctor: {obj.name_doctor_id.name}")
                for obj in self]
