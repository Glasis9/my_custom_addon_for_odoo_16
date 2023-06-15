import datetime

from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = "hospital.person"

    birth_date = fields.Date()
    age = fields.Integer(
        readonly=True,
        compute="_compute_age",
        store=True,
    )

    observing_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Observing doctor",
        ondelete="set null",
    )

    @api.depends("birth_date")
    def _compute_age(self):
        for obj in self:
            obj.age = datetime.date.today().year - obj.birth_date.year
