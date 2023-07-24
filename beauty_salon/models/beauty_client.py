from odoo import models, fields, _


class BeautyClient(models.Model):
    _name = "beauty.client"
    _description = "Client"
    _inherit = "person.mixin"

    history_visit = fields.One2many(
        comodel_name="beauty.client.visit",
        inverse_name="client_id",
    )

    def action_sign_up_master_wizard(self):
        self.ensure_one()
        return {
            "name": _("Sign up for a master"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "beauty.sign.up.master.wizard",
            "target": "new",
            "context": {
                "default_client_id": self.id,
            },
        }

    def action_find_out_discount_wizard(self):
        self.ensure_one()
        return {
            "name": _("Find out discount"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "find.out.discount.wizard",
            "target": "new",
            "context": {
                "default_client_id": self.id,
            },
        }
