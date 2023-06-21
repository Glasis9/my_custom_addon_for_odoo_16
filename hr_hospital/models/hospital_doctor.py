from odoo import models, fields, api


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

