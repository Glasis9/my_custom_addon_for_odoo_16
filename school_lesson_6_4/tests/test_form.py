import datetime

from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo.addons.school_lesson_6_4.tests.common import TestCommon


def create_book_form(self):
    return Form(self.book_demo)


@tagged('post_install', '-at_install', 'library')
class TestForm(TestCommon):

    def test_01_book_taken_date(self):
        book_form = create_book_form(self)

        book_form.reader_id = self.library_user.partner_id
        self.assertEqual(book_form.taken_date, fields.Date.today())

        book_form.reader_id = self.library_user.partner_id
        self.assertNotEqual(
            book_form.taken_date,
            fields.Date.today() + datetime.timedelta(days=1)
        )

    def test_02_default_get(self):
        book_form = create_book_form(self)

        book_form.type = "encyclopedia"
        self.assertEqual(book_form.type, "encyclopedia")
        self.assertNotEqual(book_form.type, "book")

    def test_03_default_get(self):
        book_form = create_book_form(self)

        self.assertEqual(book_form.type, "book")
