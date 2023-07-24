import datetime

from odoo import models, fields, api, exceptions, _


class BeautyMasterSchedule(models.Model):
    _name = "beauty.master.schedule"
    _description = "Master schedule"
    _rec_name = "master_id"

    master_id = fields.Many2one(
        required=True,
        comodel_name="beauty.master",
        string="Master",
    )
    free_date_time_start = fields.Datetime(
        required=True,
        string="Free time start",
        default=datetime.date.today()
    )
    free_date_time_finish = fields.Datetime(
        string="Free time finish",
        compute="_compute_finish_time"
    )

    @api.depends("free_date_time_start")
    def _compute_finish_time(self):
        for obj in self:
            if not isinstance(obj.free_date_time_start, bool):
                obj.free_date_time_finish = \
                    obj.free_date_time_start + datetime.timedelta(hours=1)

    @api.constrains("free_date_time_start")
    def _constraint_check_free_date_time_finish(self):
        for schedule in self:
            res = self.env["beauty.master.schedule"].search([
                ("master_id", "=", schedule.master_id.id),
                ("free_date_time_start", "=", schedule.free_date_time_start),
                ("id", "!=", schedule.id)
            ])
            if len(res) > 0:
                raise exceptions.ValidationError(
                    _("This time is already taken by the master, "
                      "specify another"))
