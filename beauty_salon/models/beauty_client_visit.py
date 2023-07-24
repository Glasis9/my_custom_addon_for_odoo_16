import datetime
from odoo import models, fields, api, _, exceptions


class BeautyClientVisit(models.Model):
    _name = "beauty.client.visit"
    _description = "Client Visit"

    date_time_start = fields.Datetime(
        string="Start time",
        required=True,
    )
    spent_time = fields.Selection(
        selection=[
            ("10", "10 minutes"), ("20", "20 minutes"),
            ("30", "30 minutes"), ("40", "40 minutes"),
            ("50", "50 minutes"), ("1", "1 hour"),
            ("1.5", "1 h 30 min"), ("2", "2 hours"),
            ("2.5", "2 h 30 min"), ("3", "3 hours"),
            ("3.5", "3 h 30 min"), ("4", "4 hours"),
            ("4.5", "4 h 30 min"), ("5", "5 hours"),
            ("5.5", "5 h 30 min"), ("6", "6 hours"),
            ("6.5", "6 h 30 min"), ("7", "7 hours"),
            ("7.5", "7 h 30 min"), ("8", "8 hours"),
            ("8.5", "8 h 30 min"), ("9", "9 hours"),
            ("9.5", "9 h 30 min"),
        ],
    )
    date_time_finish = fields.Datetime(
        string="Finish time",
        compute="_compute_finish_time",
        store=True,
    )
    master_id = fields.Many2one(
        required=True,
        comodel_name="beauty.master",
        string="Master",
        domain='[("speciality", "=", speciality)]',
    )
    speciality = fields.Char(compute="_compute_speciality", store=True)

    state = fields.Selection(
        readonly=True,
        selection=[("in progress", "In progress"), ("completed", "Completed")],
        default="in progress",
        store=True,
    )
    client_id = fields.Many2one(
        required=True,
        comodel_name="beauty.client",
        string="Client",
    )
    service_id = fields.Many2one(
        comodel_name="beauty.service",
        string="Service",
        required=True,
    )

    by_appointment = fields.Boolean(string="By appointment")

    price = fields.Char(
        compute="_compute_price",
        readonly=True,
        store=True,
        default=0,
    )

    @api.depends("service_id")
    def _compute_speciality(self):
        for visit in self:
            speciality = visit.service_id.category_id.name
            if isinstance(speciality, str):
                visit.speciality = visit.service_id.category_id.name.lower()
            else:
                visit.speciality = ""

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
        return [(obj.id, "%s" % obj.client_id.name) for obj in self]

    @api.depends("spent_time")
    def _compute_finish_time(self):
        for visit in self:
            if not isinstance(visit.spent_time, bool):
                if visit.spent_time in ("10", "20", "30", "40", "50"):
                    time = int(visit.spent_time)
                else:
                    time = int(float(visit.spent_time) * 60)

                visit.date_time_finish = visit.date_time_start + datetime.\
                    timedelta(minutes=time)

                if visit.date_time_finish < datetime.datetime.now():
                    visit.state = "completed"
            else:
                visit.date_time_finish = False

    def unlink(self):
        for record in self:
            if record.state == "completed" and not self.env.user.has_group(
                    "beauty_salon.group_beauty_salon_admin"
            ):
                raise exceptions.ValidationError(
                    _("You cannot delete a visit record")
                )
        return super(BeautyClientVisit, self).unlink()
