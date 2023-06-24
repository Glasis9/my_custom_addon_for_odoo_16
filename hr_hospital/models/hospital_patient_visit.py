import datetime

from odoo import models, fields, api, _, exceptions


class HospitalPatientVisit(models.Model):
    _name = "hospital.patient.visit"
    _description = "Patient Visit"

    date_time_start = fields.Datetime(
        required=True,
        readonly=False,
        states={
            "in progress": [("readonly", False)],
            "completed": [("readonly", True)],
        },
    )
    name_doctor_id = fields.Many2one(
        required=True,
        comodel_name="hospital.doctor",
        string="Doctor",
        ondelete="cascade",
        readonly=False,
        states={
            "in progress": [("readonly", False)],
            "completed": [("readonly", True)],
        },
    )
    state = fields.Selection(
        readonly=True,
        compute="_compute_date",
        selection=[("in progress", "In progress"), ("completed", "Completed")],
        default="in progress",
    )
    name_patient_id = fields.Many2one(
        required=True,
        comodel_name="hospital.patient",
        string="Patient",
        ondelete="cascade",
    )
    diagnosis_id = fields.Many2one(
        comodel_name="hospital.diagnosis",
        string="Diagnosis",
        ondelete="cascade",
    )

    by_appointment = fields.Boolean()

    def name_get(self):
        return [(obj.id, "%s" % obj.name_patient_id.name) for obj in self]

    @api.depends("date_time_start")
    def _compute_date(self):
        for visit in self:
            if visit.date_time_start < datetime.datetime.now() and \
                    visit.name_doctor_id and visit.name_patient_id:
                visit.state = "completed"
            else:
                visit.state = "in progress"

    def unlink(self):
        for record in self:
            if record.diagnosis_id and record.state == "completed":
                raise exceptions.ValidationError(
                    _("You cannot delete a visit record")
                )
        return super(HospitalPatientVisit, self).unlink()
