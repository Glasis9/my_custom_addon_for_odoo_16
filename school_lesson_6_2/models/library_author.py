import datetime

from odoo import fields, models, api


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Book Authors'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date('Birthday')

    check_date_create = fields.Boolean(compute="_compute_check_date_create")

    @api.depends("check_date_create")
    def _compute_check_date_create(self):
        date = datetime.datetime.today() - datetime.timedelta(days=30)
        for obj in self:
            if obj.create_date >= date:
                obj.check_date_create = True
            else:
                obj.check_date_create = False

    def name_get(self):
        return [(rec.id, "%s %s" % (
            rec.first_name, rec.last_name)) for rec in self]

    def action_delete(self):
        self.ensure_one()
        self.check_access_rights('unlink')
        self.unlink()

    def _create_by_user(self, vals):
        return self.sudo().create(vals)
