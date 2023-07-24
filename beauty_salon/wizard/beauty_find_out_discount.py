from odoo import models, fields, api, _


class FindOutDiscount(models.TransientModel):
    _name = "find.out.discount.wizard"
    _description = "Find out discount"

    discount = fields.Char(compute="_compute_discount")
    text = fields.Char()

    client_id = fields.Many2one(
        comodel_name="beauty.client",
    )

    @api.depends("client_id")
    def _compute_discount(self):
        for record in self:
            visits = self.env["beauty.client.visit"].search([
                ("client_id", "=", self.client_id.id),
                ("state", "=", "completed"),
            ])
            total_costs = 0
            for vis in visits:
                if vis.price != "Free":
                    total_costs += float(vis.price.split()[0])

            if 100 <= total_costs <= 150:
                record.discount = "10%"
                record.text = _("Your spent more than 100$, your discount 10%")
            elif total_costs > 150:
                record.discount = "15%"
                record.text = _("Your spent more than 150$, your discount 15%")
            else:
                record.discount = "0%"
                record.text = _("For 100$ spent on services - "
                                "your discount will be 10%, for 150$ your "
                                "discount will be 15%")
