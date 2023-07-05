import datetime

from odoo import models, fields, _, api, exceptions


class HospitalAddMakingAppointmentWizard(models.TransientModel):
    _name = "hospital.add.making.appointment.wizard"
    _description = "Add making appointment"
    _rec_name = "name_patient_id"

    doctor_id = fields.Many2one(
        required=True,
        comodel_name="hospital.doctor",
        string="Doctor name",
        ondelete="cascade",
    )
    available_date_time = fields.Char(
        string="Available dates and hours",
        readonly=True,
        store=True,
    )
    date_time_appointment = fields.Datetime(
        required=True,
        string="Date and time of appointment",
    )
    name_patient_id = fields.Many2one(
        required=True,
        comodel_name="hospital.patient",
        string="Patient",
        ondelete="cascade",
    )

    def name_get(self):
        return [(obj.id, f"Patient: {obj.name_patient_id.name}, "
                         f"Doctor: {obj.doctor_id.name}")
                for obj in self]

    @api.onchange("doctor_id")
    def _onchange_doctor_id(self):
        for obj in self:
            available_date_time = self.env["hospital.allocation.doctor"] \
                .search(
                [
                    ("doctor_id", "=", obj.doctor_id.id),
                    ("date_time_receipt", ">=", datetime.datetime.now()),
                ]
            )
            if len(available_date_time) != 0:
                record_str = [str(rec.date_time_receipt +
                                  datetime.timedelta(hours=3))
                              for rec in available_date_time]

                obj.available_date_time = record_str
            else:
                obj.available_date_time = "This doctor does not have free " \
                                          "appointments, choose another doctor"

    def add_appointment(self):
        for obj in self:
            available_date_time = self.env["hospital.allocation.doctor"] \
                .search(
                [
                    ("doctor_id", "=", obj.doctor_id.id),
                    ("date_time_receipt", ">=", datetime.datetime.now()),
                ]
            )
            record = [rec.date_time_receipt for rec in available_date_time]
            if obj.date_time_appointment not in record:
                raise exceptions.ValidationError(
                    _("Select an available date and time")
                )

            obj.env["hospital.patient.visit"].create(
                {
                    "name_doctor_id": obj.doctor_id.id,
                    "date_time_start": obj.date_time_appointment,
                    "name_patient_id": obj.name_patient_id.id,
                    "by_appointment": True,
                }
            )
            return {
                "name": _("Patient visit"),
                "type": "ir.actions.act_window",
                "view_mode": "tree",
                "res_model": "hospital.patient.visit",
                "target": "current",
            }
