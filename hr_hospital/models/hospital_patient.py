import datetime

from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Patient"
    _inherit = "hospital.person"

    birth_date = fields.Date()
    age = fields.Char(
        readonly=True,
        compute="_compute_age",
        store=True,
    )
    passport_data = fields.Char()
    contact_person_id = fields.Many2one(
        comodel_name="hospital.contact.person",
        string="Contact person",
        ondelete="set null",
    )
    observing_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Observing doctor",
        ondelete="cascade",
    )

    @api.depends("birth_date")
    def _compute_age(self):
        for obj in self:
            if isinstance(obj.birth_date, datetime.date):
                obj.age = int(
                    (datetime.date.today() - obj.birth_date).days / 365
                )

    def write(self, vals):
        for patient in self:
            self.env["hospital.history.changing.personal.doctor"].create(
                {
                    "choice_doctor_date_time": datetime.datetime.now(),
                    "name_patient_id": patient.id,
                    "name_doctor_id": patient.observing_doctor_id.id,
                 }
            )
        return super(HospitalPatient, self).write(vals)
