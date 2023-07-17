from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestEmailUnique(TransactionCase):

    def setUpClass(self):
        super(TestEmailUnique, self).setUpClass()
        self.partner_1 = self.env["res.partner"].create(
            {"name": "Partner 1", "email": "test@test.com"}
        )

    def test_create_partner_with_duplicate_email(self):
        with self.assertRaises(ValidationError):
            self.partner_2 = self.env["res.partner"].create(
                {"name": "Partner 2", "email": "test@test.com"}
            )

    def test_write_partner_duplicate_email(self):
        self.partner_3 = self.env["res.partner"].create(
            {"name": "Partner 3", "email": "test_partner_3@test.com"}
        )
        with self.assertRaises(ValidationError):
            self.partner_3.write({"email": "test@test.com"})
