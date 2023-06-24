from odoo import models, fields, _


class HospitalDiseaseReportWizard(models.TransientModel):
    _name = "hospital.disease.report.wizard"
    _description = "Disease report"

    month_year = fields.Date(string="Year and month")

    disease_id = fields.Many2one(
        comodel_name="hospital.disease"
    )

    count_diagnosis = fields.Integer()
    diagnosis_id = fields.Many2one(
        comodel_name="hospital.diagnosis"
    )

    def action_disease_report(self):
        for rec in self:
            diagnosis = []
            if rec.disease_id and rec.month_year:
                diagnosis_all = self.env["hospital.diagnosis"].search([
                    ("disease_ids", "in", [rec.disease_id.id])
                ])
                for diagnos in diagnosis_all:
                    if diagnos.date_diagnosis.year == \
                            rec.month_year.year and \
                            diagnos.date_diagnosis.month == \
                            rec.month_year.month:
                        diagnosis.append(diagnos.id)

            if rec.disease_id:
                diagnos = self.env["hospital.diagnosis"].search([
                    ("disease_ids", "in", [rec.disease_id.id])
                ])
                for diag in diagnos:
                    diagnosis.append(diag.id)

            if rec.month_year:
                diagnosis_all = self.env["hospital.diagnosis"].search([])

                for diagnos in diagnosis_all:
                    if diagnos.date_diagnosis.year == \
                            rec.month_year.year and \
                            diagnos.date_diagnosis.month == \
                            rec.month_year.month:
                        diagnosis.append(diagnos.id)

            return {
                "name": _("Disease report"),
                "type": "ir.actions.act_window",
                "view_mode": "tree",
                "res_model": "hospital.diagnosis",
                "target": "new",
                "domain": [
                    ("id", "in", diagnosis)
                ],
            }
