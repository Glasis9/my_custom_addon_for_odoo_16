from odoo import models, fields, _, api, exceptions


class BeautyMaster(models.Model):
    _name = "beauty.master"
    _description = "Beauty master"
    _inherit = "person.mixin"
    _rec_name = "name"

    speciality = fields.Selection(
        required=True,
        selection=[
            ("hairdresser", "Hairdresser"),
            ("browist", "Browist"),
            ("visagiste", "Visagiste"),
            ("manicurist", "Manicurist"),
            ("masseur", "Masseur"),
            ("beautician", "Beautician"),
        ]
    )

    master_id = fields.Many2one(
        string="Master name",
        comodel_name="beauty.master",
        readonly=True,
        states={
            "master": [("invisible", True), ("required", False)],
            "trainee": [("required", True), ("readonly", False)],
        },
        domain=[("state", "=", "master"), ("trainee_id", "=", False)]
    )
    trainee_id = fields.Many2one(
        string="Trainee name",
        comodel_name="beauty.master",
        readonly=True,
        states={
            "master": [("readonly", False)],
            "trainee": [("invisible", True)],
        },
        domain=[("state", "=", "trainee"), ("master_id", "=", False)]
    )
    state = fields.Selection(
        string="Qualification",
        selection=[("master", "Master"), ("trainee", "Trainee")],
        required=True,
        store=True,
    )
    master_one2many_id = fields.One2many(
        comodel_name="beauty.master",
        inverse_name="master_id",
    )
    trainee_one2many_id = fields.One2many(
        comodel_name="beauty.master",
        inverse_name="trainee_id",
    )
    client_one2many_id = fields.One2many(
        comodel_name="beauty.client.visit",
        inverse_name="master_id",
    )

    @api.constrains("age")
    def check_age(self):
        for person in self:
            if person.age < 18 or person.age > 50:
                raise exceptions.ValidationError(
                    _("The age of the master cannot be less than 18 and more "
                      "than 50 years old")
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
                "default_master_id": self.id,
            },
        }
