from odoo import api, models, exceptions, _


class UniquenessPartnerMail(models.Model):
    _inherit = "res.partner"

    @api.constrains("email")
    def check_email_unique(self):
        for partner in self:
            if (self.search_count([
                ("email", "=", partner.email), ("id", "!=", partner.id)
            ]) > 0):
                raise exceptions.ValidationError(
                    _("This email is already in the system, please enter "
                      "another one")
                )

    # @api.model_create_multi
    # def create(self, vals_list):
    #     if "email" in vals_list[0]:
    #         check_email(self, vals_list[0]["email"])
    #         return super(UniquenessPartnerMail, self).create(vals_list)
    #
    # def write(self, vals_dict):
    #     if "email" in vals_dict:
    #         check_email(self, vals_dict["email"])
    #         return super(UniquenessPartnerMail, self).write(vals_dict)

# def check_email(self, vals: list | dict) -> None:
#     partners = self.env["res.partner"].search([])
#     emails = [partner.email for partner in partners]
#     if vals in emails:
#         raise exceptions.ValidationError(_("This email is already in the "
#                                          "system, please enter another one"))
