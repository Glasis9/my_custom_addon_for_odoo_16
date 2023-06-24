from odoo import models, fields, _


class HospitalDiseaseReportWizard(models.TransientModel):
    _name = "hospital.disease.report.wizard"
    _description = "Disease report"

    year = fields.Date(required=True)
    month = fields.Date(required=True)

    disease = fields.Many2one(
        comodel_name="hospital.disease"
    )
    count_disease = fields.Integer()

    def disease_report(self):
        for record in self:
            pass



    # def action_disease_report(self):
    #     doctor_ids = [rec.observing_doctor_id.id for rec in self]
    #     return {
    #         "name": _("Change doctor"),
    #         "type": "ir.actions.act_window",
    #         "view_mode": "form",
    #         "res_model": "hospital.change.doctor.wizard",
    #         "target": "new",
    #         "context": {
    #             "default_doctor_ids": doctor_ids,
    #         },
    #     }
