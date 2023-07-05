from odoo import models, fields


class HospitalChangeDoctorWizard(models.TransientModel):
    _name = "hospital.change.doctor.wizard"
    _description = "Change doctor multi"

    doctor_ids = fields.Many2many(
        string="Old doctors",
        comodel_name="hospital.doctor",
    )

    change_doctor_id = fields.Many2one(
        required=True,
        comodel_name="hospital.doctor",
        string="New doctor",
        ondelete="cascade",
    )

    def change_doctor(self):
        for record in self:
            for patient in record.patient_ids:
                pat = self.env["hospital.patient"].search([
                    ("id", "=", patient.id)
                ])
                pat.observing_doctor_id = record.change_doctor_id.id
