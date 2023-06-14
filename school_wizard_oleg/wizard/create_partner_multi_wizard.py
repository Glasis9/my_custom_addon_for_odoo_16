from odoo import _, fields, models


class CreatePartnerMultiWizard(models.TransientModel):
    _name = "create.partner.multi.wizard"
    _description = "Wizard to create partners in easy way"

    names = fields.Char(string="Partner Names")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
    )
    company_type = fields.Selection(
        [("person", "Individual"), ("company", "Company")],
        string="Company Type",
        default="person",
    )

    # Метод, который будет вызывать визард и создавать новое окно
    # Нужен, что бы мы могли добавить вызов этого визарда в любом меню системы
    def action_open_wizard(self):
        return {
            "name": _("Create Partners Wizard"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "create.partner.multi.wizard",  # имя текущей модели wizard
            "target": "new",  # new - всплывающие окно (используется для wizard)
            # current - обычное текущее окно
            "context": {"default_country_id": self.env.user.company_id.id},
            # можем задать значения по умолчанию для некоторых полей
            # например для поля country_id по умолчанию будем передавать значение
            # страны которая установлена у текущего пользователя системы
        }

    def action_create(self):
        self.ensure_one()
        for name in self.names.split(","):
            self.env["res.partner"].create(
                {
                    "name": name,
                    "company_type": self.company_type,
                    "country_id": self.country_id.id,
                }
            )
