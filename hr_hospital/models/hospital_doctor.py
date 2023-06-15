from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctors"

    name = fields.Char(string="Full name", required=True)
