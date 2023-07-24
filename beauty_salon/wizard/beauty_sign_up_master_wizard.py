import datetime

from odoo import models, fields, _, api, exceptions


class BeautySignUpMasterWizard(models.TransientModel):
    _name = "beauty.sign.up.master.wizard"
    _description = "Sign up for a master"
    _rec_name = "client_id"

    client_id = fields.Many2one(
        required=True,
        comodel_name="beauty.client",
        string="Client",
    )
    master_id = fields.Many2one(
        required=True,
        comodel_name="beauty.master",
        string="Master",
        domain='[("speciality", "=", speciality)]',
    )
    service_id = fields.Many2one(
        required=True,
        comodel_name="beauty.service",
        string="Service",
    )

    available_date_time = fields.Char(
        string="Available dates and hours",
        readonly=True,
        store=True,
    )
    date_time_record = fields.Datetime(
        required=True,
        string="Date and time of record",
    )

    speciality = fields.Char(
        compute="_compute_speciality",
        store=True,
        default="",
    )

    price = fields.Char(
        compute="_compute_price",
        readonly=True,
        store=True,
        default=0,
    )
    by_appointment = fields.Boolean(string="By appointment", default=True)

    @api.depends("service_id")
    def _compute_speciality(self):
        for visit in self:
            speciality = visit.service_id.category_id.name
            if isinstance(speciality, str):
                visit.speciality = visit.service_id.category_id.name.lower()

    @api.depends("master_id")
    def _compute_price(self):
        for visit in self:
            if visit.master_id.state != "trainee":
                visits = self.env["beauty.client.visit"].search([
                    ("client_id.name", "=", visit.client_id.name),
                    ("state", "=", "completed"),
                ])

                total_costs = 0
                for vis in visits:
                    if vis.price != "Free":
                        total_costs += float(vis.price.split()[0])

                price = int(visit.service_id.price.split()[0])
                if 100 <= total_costs <= 150:
                    visit.price = f"{price - (price * 0.1)}"
                elif total_costs > 150:
                    visit.price = f"{price - (price * 0.15)}"
                else:
                    visit.price = price
            else:
                visit.price = "Free"

    def name_get(self):
        return [(obj.id, f"Client: {obj.client_id.name}, "
                         f"Master: {obj.master_id.name}")
                for obj in self]

    @api.onchange("master_id")
    def _onchange_master_id(self):
        for obj in self:
            available_date_time = self.env["beauty.master.schedule"].search(
                [
                    ("master_id", "=", obj.master_id.id),
                    ("free_date_time_start", ">=", datetime.datetime.now()),
                ]
            )
            if len(available_date_time) != 0:
                record_str = [str(rec.free_date_time_start +
                                  datetime.timedelta(hours=3))
                              for rec in available_date_time]

                obj.available_date_time = record_str
            else:
                obj.available_date_time = "This master has no free places " \
                                          "for recording, please choose " \
                                          "another master"

    def sign_up_for_master(self):
        for obj in self:
            available_date_time = self.env["beauty.master.schedule"].search(
                [
                    ("master_id", "=", obj.master_id.id),
                    ("free_date_time_start", ">=", datetime.datetime.now()),
                ]
            )
            record = [rec.free_date_time_start for rec in available_date_time]
            if obj.date_time_record not in record:
                raise exceptions.ValidationError(
                    _("Select an available date and time")
                )

            obj.env["beauty.client.visit"].create(
                {
                    "client_id": obj.client_id.id,
                    "service_id": obj.service_id.id,
                    "master_id": obj.master_id.id,
                    "date_time_start": obj.date_time_record,
                    "by_appointment": True,
                }
            )
            return {
                "name": _("Client visit"),
                "type": "ir.actions.act_window",
                "view_mode": "tree",
                "res_model": "beauty.client.visit",
                "target": "current",
                "domain": [("client_id", "=", obj.client_id.id)]
            }
