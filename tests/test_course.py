from odoo.tests.common import TransactionCase


class TestCourse(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestCourse, self).setUp()

        self.course_test_record = self.env['test_app.course'].create({
            'name': 'course_test_record',
            'description': 'course_test_record',
            'summary': 'course_test_record',
            # 'responsible_id' : fields.Many2one("res.users", ondelete:"set null", string:"Presenter", index:True, tracking:1)
            # session_ids : fields.One2many("test_app.session", "course_id", string:"Sessions")
            'state': 'opened',
            'active': True,
            # expiration_date : fields.Date(tracking:1)
            'is_expired': True
        })

    def test_01_course_values(self):
        course_id = self.course_test_record
        self.assertRecordValues(course_id, [{
            'name': 'course_test_record',
            'description': 'course_test_record',
            'summary': 'course_test_record',
            # 'responsible_id' : fields.Many2one("res.users", ondelete:"set null", string:"Presenter", index:True, tracking:1)
            # session_ids : fields.One2many("test_app.session", "course_id", string:"Sessions")
            'state': 'opened',
            'active': True,
            # expiration_date : fields.Date(tracking:1)
            'is_expired': True
        }])

