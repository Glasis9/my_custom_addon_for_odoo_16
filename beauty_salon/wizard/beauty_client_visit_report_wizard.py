from odoo import models, fields, _


class BeautyClientVisitReportWizard(models.TransientModel):
    _name = "beauty.client.visit.report.wizard"
    _description = "Client visit report"

    month_year = fields.Date(string="Year and month", required=True)

    service_id = fields.Many2one(
        comodel_name="beauty.service"
    )
    client_id = fields.Many2one(
        comodel_name="beauty.client"
    )
    master_id = fields.Many2one(
        comodel_name="beauty.master"
    )

    def action_client_visit_report(self):
        for rec in self:
            all_visits = self.env["beauty.client.visit"].search([])

            visits = [
                visit
                for visit in all_visits
                if visit.date_time_start.month == rec.month_year.month
            ]

            filter_visits = []
            for visit in visits:
                if rec.service_id and visit.service_id == rec.service_id:
                    filter_visits.append(visit.id)
                if rec.client_id and visit.client_id == rec.client_id:
                    filter_visits.append(visit.id)
                if rec.master_id and visit.master_id == rec.master_id:
                    filter_visits.append(visit.id)

            if len(filter_visits) == 0:
                list_visits = [visit.id for visit in visits]
            else:
                list_visits = filter_visits
            return {
                "name": _("Client visit report"),
                "type": "ir.actions.act_window",
                "view_mode": "tree",
                "res_model": "beauty.client.visit",
                "target": "new",
                "domain": [("id", "in", list_visits)],
            }
