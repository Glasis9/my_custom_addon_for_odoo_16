import datetime

from odoo import models, fields, _, exceptions, api


class BeautySaloonPersonMixin(models.AbstractModel):
    _name = "person.mixin"
    _inherit = "avatar.mixin"
    _description = "Personality Information Mixin"

    name = fields.Char(
        string="Full name",
        required=True,
        help="Example: Usenko Oleg",
    )
    email = fields.Char(help="Example: example@gmail.com")
    phone = fields.Char(help="Example: 0123456789", unaccent=False)
    birth_date = fields.Date(required=True)
    age = fields.Integer(
        readonly=True,
        compute="_compute_age",
        store=True,
    )
    gender = fields.Selection(
        selection=[("male", _("Male")), ("female", _("Female"))],
        required=True,
    )

    @api.depends("birth_date")
    def _compute_age(self):
        for obj in self:
            if isinstance(obj.birth_date, datetime.date):
                obj.age = int(
                    (datetime.date.today() - obj.birth_date).days / 365
                )
            else:
                obj.age = 0

    @api.constrains("email")
    def check_email_unique(self):
        for person in self:
            if (self.search_count([
                ("email", "=", person.email), ("id", "!=", person.id)
            ]) > 0):
                raise exceptions.ValidationError(
                    _("This email is already in the system, please enter "
                      "another one")
                )

    @api.constrains("phone")
    def check_phone(self):
        for person in self:
            if person.phone:
                if len(person.phone) != 10:
                    raise exceptions.ValidationError(
                        _("Mobile phone number must contain 10 digits")
                    )
                if not person.phone.isdigit():
                    raise exceptions.ValidationError(
                        _("Mobile phone number must contain only digits")
                    )
