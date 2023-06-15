from odoo import models, fields, _


class HospitalPerson(models.AbstractModel):
    _name = "hospital.person"
    _description = "Personality information mixin"

    name = fields.Char(string="Full name", required=True)
    phone = fields.Integer()
    email = fields.Char()
    photo = fields.Binary(attachment=False)
    gender = fields.Selection(
        default="other",
        selection=[
            ("male", _("Male")), ("female", _("Female")),
            ("other", _("Other / Undefined"))
        ],
    )
