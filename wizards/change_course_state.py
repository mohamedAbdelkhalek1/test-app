from odoo import models, fields
from odoo.exceptions import ValidationError


class ChangeCourseState(models.TransientModel):
    _name = 'test_app.change_course_state'
    _description = 'test_app.change_course_state'

    user_id = fields.Many2one('res.users', string="User")
    course_id = fields.Many2one('test_app.course', string="Course")
    old_state = fields.Selection([('opened', 'Opened'), ('closed', 'Closed')])
    new_state = fields.Selection([('opened', 'Opened'), ('closed', 'Closed')])
    description = fields.Char()

    def change_course_state_confirm(self):
        self.course_id.state = self.new_state
        if self.old_state != self.new_state:
            self.course_id.create_new_history(self.old_state, self.new_state)
        else:
            raise ValidationError(f"already has a {self.old_state} state.")
        # for rec in self:
        #     rec.env['test_app.history'].create({
        #         'user_id': rec.user_id,
        #         'course_id': rec.course_id,
        #         'old_state': rec.old_state,
        #         'new_state': rec.new_state,
        #         # 'description': 'A user ' + str(rec.user_id) + ' changed the course ' + str(rec.course_id) + ' from ' + rec.old_state + ' to ' + rec.new_state
        #     })
