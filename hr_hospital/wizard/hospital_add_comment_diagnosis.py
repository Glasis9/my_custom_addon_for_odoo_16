from odoo import models, fields, _


class HospitalAddCommentDiagnosisWizard(models.TransientModel):
    _name = "hospital.add.comment.diagnosis"
    _description = "Add comment to the diagnosis"

    comment = fields.Text()

    def update_field_comment_diagnosis(self):
        for obj in self:
            obj.env["hospital.diagnosis"].update(
                {
                    "comment": obj.comment,
                }
            )

    @staticmethod
    def action_add_comment():
        return {
            "name": _("Add comment by Doctor-Mentor"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "hospital.add.comment.diagnosis",
            "target": "new",
        }
