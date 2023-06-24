from odoo import models, fields, api, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Doctors"
    _inherit = "hospital.person"

    speciality = fields.Char(required=True, default="Undefined")

    intern = fields.Boolean(required=True)
    mentor = fields.Boolean(compute="_check_intern")

    @api.depends("intern")
    def _check_intern(self):
        for doctor in self:
            if doctor.intern:
                doctor.mentor = False
            else:
                doctor.mentor = True

    # def action_disease_report(self):
    #     # doctor_ids = [rec.observing_doctor_id.id for rec in self]
    #     for record in self:
    #         return {
    #             "name": _("Disease report"),
    #             "type": "ir.actions.act_window",
    #             "view_mode": "form",
    #             "res_model": "hospital.disease.report.wizard",
    #             "target": "new",
    #             # "context": {
    #             #     "default_doctor_ids": doctor_ids,
    #             # },
    #         }
