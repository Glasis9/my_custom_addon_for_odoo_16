import datetime

from odoo import models, fields, api, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Patient"
    _inherit = "hospital.person"

    birth_date = fields.Date(required=True)
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

    diagnosis_id = fields.One2many(
        comodel_name="hospital.diagnosis",
        inverse_name="name_patient_id",
    )

    analysis_id = fields.One2many(
        comodel_name="hospital.analysis",
        inverse_name="name_patient_id",
    )

    @api.depends("birth_date")
    def _compute_age(self):
        for obj in self:
            if isinstance(obj.birth_date, datetime.date):
                obj.age = int(
                    (datetime.date.today() - obj.birth_date).days / 365
                )
            else:
                obj.age = 0

    def write(self, vals):
        for patient in self:
            self.env["hospital.history.changing.personal.doctor"].create({
                "choice_doctor_date_time": datetime.datetime.now(),
                "name_patient_id": patient.id,
                "name_doctor_id": patient.observing_doctor_id.id,
            })
        return super(HospitalPatient, self).write(vals)

    def action_change_doctor(self):
        doctor_ids = [rec.observing_doctor_id.id for rec in self]
        return {
            "name": _("Change doctor"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "hospital.change.doctor.wizard",
            "target": "new",
            "context": {
                "default_doctor_ids": doctor_ids,
            },
        }

    def action_history_patient_visit(self):
        for patient in self:
            return {
                "name": _("History patient visit"),
                "type": "ir.actions.act_window",
                "view_mode": "tree",
                "res_model": "hospital.patient.visit",
                "target": "new",
                "domain": [("name_patient_id.id", "=", patient.id)]
            }

    def action_make_appointment_to_doctor_wizard(self):
        for patient in self:
            return {
                "name": _("Make appointment to doctor"),
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "hospital.add.making.appointment.wizard",
                "target": "new",
                "context": {
                    "default_name_patient_id": patient.id,
                },
            }
