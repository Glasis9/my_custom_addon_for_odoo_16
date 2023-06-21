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
    date_receipt = fields.Date(
        required=True,
        string="Date of receipt",
        default=fields.date.today(),
    )
    time_receipt = fields.Float(string="Time")

    @api.onchange("time_receipt")
    def _onchange_time_receipt(self):
        for obj in self:
            res = self.env["hospital.allocation.doctor"].search([])
            res = res.filtered(lambda r: r.doctor_id == obj.doctor_id and
                                         r.date_receipt == obj.date_receipt and
                                         r.id != obj.id
                               )
            for time in res:
                if obj.time_receipt == time["time_receipt"]:
                    raise exceptions.ValidationError(
                        _("This appointment time is already taken, "
                          "please specify another"))

    def write(self, vals):
        for obj in self:
            res = self.env["hospital.allocation.doctor"].search([])
            res = res.filtered(lambda r: r.doctor_id == obj.doctor_id and
                                         r.date_receipt == obj.date_receipt and
                                         r.id != obj.id
                               )
            for time in res:
                if obj.time_receipt == time["time_receipt"]:
                    raise exceptions.ValidationError(
                        _("This appointment time is already taken, "
                          "please specify another"))
        return super(HospitalAllocationDoctor, self).write(vals)
