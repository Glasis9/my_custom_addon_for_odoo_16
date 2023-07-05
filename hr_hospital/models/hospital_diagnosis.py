from odoo import models, fields, _, api, exceptions


class HospitalDiagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "Diagnosis"
    _rec_name = "name_patient_id"

    name_patient_id = fields.Many2one(
        required=True,
        comodel_name="hospital.patient",
        string="Name patient",
        ondelete="cascade",
    )
    observing_doctor_id = fields.Many2one(
        required=True,
        comodel_name="hospital.doctor",
        string="Observing doctor",
        ondelete="cascade",
    )
    disease_ids = fields.Many2many(
        comodel_name="hospital.disease",
        string="Disease",
    )
    date_diagnosis = fields.Date(
        required=True,
        string="Date of diagnosis",
        default=fields.date.today(),
    )
    prescription = fields.Char(string="Doctor's appointment")
    comment = fields.Text(help="Commentary from the Doctor-Mentor")

    # category_disease = fields.Char(
    #     related="disease_ids.category_id.name",
    #     store=True
    # )

    def name_get(self):
        return [
            (obj.id, "%s, %s" % (obj.name_patient_id.name, obj.date_diagnosis))
            for obj in self
        ]

    @api.constrains("comment")
    def _constrains_comment(self):
        for diagnosis in self:
            if diagnosis.observing_doctor_id.doctor_mentor and \
                    not diagnosis.comment:
                raise exceptions.ValidationError(
                    _(f"Doctor-mentor: "
                      f"{diagnosis.observing_doctor_id.doctor_mentor.name} "
                      f"must add a comment to the diagnosis!")
                )
