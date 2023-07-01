from odoo import models, fields, api, _, exceptions


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Doctors"
    _inherit = "hospital.person"
    _rec_name = "name"

    speciality = fields.Char(required=True, default="Undefined")

    doctor_mentor_id = fields.Many2one(
        string="Mentor name",
        comodel_name="hospital.doctor",
        readonly=True,
        required=False,
        states={
            "no intern": [("readonly", True), ("required", False)],
            "intern": [("readonly", False), ("required", True)],
        },
        domain=[("state", "=", "no intern")]
    )
    intern_id = fields.Many2one(
        string="Intern name",
        comodel_name="hospital.doctor",
        readonly=True,
        required=False,
        states={
            "no intern": [("readonly", False)],
            "intern": [("readonly", True)],
        },
        domain=[("state", "=", "intern")]
    )
    state = fields.Selection(
        string="Intern",
        selection=[("intern", "Intern"), ("no intern", "No intern")],
        default="no intern",
        store=True,
    )
    doctor_mentor_one2many_id = fields.One2many(
        comodel_name="hospital.doctor",
        inverse_name="doctor_mentor_id",
    )
    intern_one2many_id = fields.One2many(
        comodel_name="hospital.doctor",
        inverse_name="intern_id",
    )
    patient_one2many_id = fields.One2many(
        comodel_name="hospital.patient",
        inverse_name="observing_doctor_id",
    )

    def action_make_appointment_to_doctor_wizard(self):
        for doctor in self:
            return {
                "name": _("Make appointment to doctor"),
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "hospital.add.making.appointment.wizard",
                "target": "new",
                "context": {
                    "default_doctor_id": doctor.id,
                },
            }

    # @api.model
    # def create(self, vals_list):
    #     doctor = self.env["hospital.doctor"].search([
    #         ("id", "=", vals_list.get("doctor_mentor"))
    #     ])
    #     if vals_list.get("state") == "intern" and doctor.state == "intern":
    #         raise exceptions.ValidationError(
    #             _("An intern cannot be a mentor, Choose another doctor to be "
    #               "your mentor"))
    #     return super(HospitalDoctor, self).create(vals_list)

    # def write(self, vals):
    #     res = super(HospitalDoctor, self).write(vals)
    #     for doc in self:
    #         if doc.state == "intern":
    #             doctor = self.env["hospital.doctor"].search([
    #                 ("id", "=", doc.doctor_mentor.id)
    #             ])
    #             if doctor.doctor_mentor.doctor_mentor:
    #                 raise exceptions.ValidationError(
    #                     _("An intern cannot be a mentor, "
    #                       "Choose another doctor to be your mentor"))
    #             elif doc.name == doctor.name:
    #                 raise exceptions.ValidationError(
    #                     _("You can't choose yourself"))
    #         return res
