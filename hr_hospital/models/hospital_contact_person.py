from odoo import models


class HospitalContactPerson(models.Model):
    _name = "hospital.contact.person"
    _description = "Contact Person"
    _inherit = "hospital.person"
    _rec_name = "name"
