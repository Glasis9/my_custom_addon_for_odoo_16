from odoo import fields, models, api, exceptions, _


class BeautyService(models.Model):
    _name = "beauty.service"
    _description = "Beauty Service"
    _rec_name = "service"

    service = fields.Char(required=True)

    category_id = fields.Many2one(
        required=True,
        comodel_name="beauty.service.category",
    )

    price = fields.Char(required=True, default=0)

    @api.onchange("price")
    def _onchange_price(self):
        self.ensure_one()
        try:
            price = int(self.price.split()[0])
        except ValueError:
            raise exceptions.ValidationError(
                _("The price field must contain only a number")
            )
        self.price = f"{price} USD"

    def name_get(self):
        return [
            (obj.id, "%s, %s" % (
                obj.service, f"category: {obj.category_id.name}"
            )) for obj in self]
