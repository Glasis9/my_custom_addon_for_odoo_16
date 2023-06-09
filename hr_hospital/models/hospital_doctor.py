import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctors"

    name = fields.Char(string="Full name", required=True)
