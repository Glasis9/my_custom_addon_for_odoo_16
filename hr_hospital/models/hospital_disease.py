from odoo import fields, models


class HospitalDisease(models.Model):
    _name = "hospital.disease"
    _description = "Disease"
    _rec_name = "disease"

    disease = fields.Char(required=True)

    category_id = fields.Many2one(
        comodel_name="hospital.disease.category",
    )

    def name_get(self):
        return [
            (obj.id, "%s, %s" % (
                obj.disease, f"category: {obj.category_id.name}"
            )) for obj in self]
