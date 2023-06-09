import logging

from odoo import models, fields


_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"

    name = fields.Char(string="Full name", required=True)

    observing_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Observing doctor",
        ondelete="set null",
    )
