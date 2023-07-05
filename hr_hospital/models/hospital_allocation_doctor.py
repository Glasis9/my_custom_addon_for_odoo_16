import datetime

from odoo import models, fields, api, exceptions, _


class HospitalAllocationDoctor(models.Model):
    _name = "hospital.allocation.doctor"
    _description = "Allocation of the doctor"
    _rec_name = "doctor_id"

    doctor_id = fields.Many2one(
        required=True,
        comodel_name="hospital.doctor",
        string="Doctor name",
        ondelete="cascade",
    )
    date_time_receipt = fields.Datetime(
        required=True,
        string="Date and time of receipt",
        default=fields.date.today(),
    )
    date_time_finish = fields.Datetime(
        compute="_compute_finish_time"
    )

    @api.depends("date_time_finish")
    def _compute_finish_time(self):
        for obj in self:
            obj.date_time_finish = obj.date_time_receipt + datetime.timedelta(
                minutes=30
            )

    @api.model
    def create(self, vals_list):
        res = self.env["hospital.allocation.doctor"].search([
            ("doctor_id", "=", vals_list.get("doctor_id")),
            ("date_time_receipt", "=", vals_list.get("date_time_receipt")),
            ("id", "!=", vals_list.get("id"))
        ])
        if len(res) > 0:
            raise exceptions.ValidationError(
                _("This appointment time is already taken, "
                  "please specify another"))
        return super(HospitalAllocationDoctor, self).create(vals_list)

    def write(self, vals):
        res = super(HospitalAllocationDoctor, self).write(vals)
        for obj in self:
            res = self.env["hospital.allocation.doctor"].search([
                ("doctor_id", "=", obj.doctor_id.id),
                ("date_time_receipt", "=", obj.date_time_receipt),
                ("id", "!=", obj.id)
            ])
            if len(res) > 0:
                raise exceptions.ValidationError(_("This appointment time is "
                                                   "already taken, please "
                                                   "specify another"))
        return res
