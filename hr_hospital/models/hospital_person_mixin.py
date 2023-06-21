from odoo import models, fields, _


class HospitalPersonMixin(models.AbstractModel):
    _name = "hospital.person"
    _description = "Personality Information Mixin"

    name = fields.Char(string="Full name", required=True)
    phone = fields.Char()
    email = fields.Char()
    photo = fields.Binary(attachment=False)
    gender = fields.Selection(
        default="other",
        selection=[
            ("male", _("Male")), ("female", _("Female")),
            ("other", _("Other / Undefined"))
        ],
    )
