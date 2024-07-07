# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
import random
from datetime import timedelta


class TestModel(models.Model):
    _name = 'test_app.test_app'
    _description = 'test_app.test_app'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100


class Course(models.Model):
    _name = 'test_app.course'
    _description = 'course'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, tracking=1, translate=1)
    description = fields.Text()
    summary = fields.Char()
    responsible_id = fields.Many2one("res.users", ondelete="set null", string="Presenter", index=True, tracking=1)
    session_ids = fields.One2many("test_app.session", "course_id", string="Sessions")
    state = fields.Selection([('opened', 'Opened'), ('closed', 'Closed')], tracking=1)
    active = fields.Boolean(default=True)
    expiration_date = fields.Date(tracking=1)
    is_expired = fields.Boolean()

    def set_course_open(self):
        self.state = 'opened'

    def set_course_close(self):
        self.state = 'closed'

    @api.model
    def create(self, vals):
        if vals['description']:
            desc_split = vals['description'].split()
            vals['summary'] = desc_split[0][0] + "." + desc_split[1] + " ..."
        return super().create(vals)  # or super(Course, self).create(vals)

    def write(self, vals):
        if 'description' in vals:
            desc_split = vals['description'].split()
            vals['summary'] = desc_split[0][0] + "." + desc_split[1] + " ..."

        super().write(vals)

    def unlink(self):
        for record in self:
            if record.state == 'opened':
                raise exceptions.UserError("Cannot Delete an opened course")
        return super().unlink()

    def action_closed(self):
        for rec in self:
            self.state = 'closed'

    def check_expired_course_date(self):
        course_ids = self.search([])
        for rec in course_ids:
            if rec.state == 'opened' and rec.expiration_date and rec.expiration_date < fields.Date.today():
                rec.is_expired = True

    def action_open_change_wizard(self):
        action = self.env.ref('test_app.change_course_state_action_view').read()[0]
        # action = self.env['ir.actions']._for_xml_id('test_app.change_course_state_action_view')
        action['context'] = {
            'default_course_id': self.id,
            'default_old_state': self.state,
            'default_user_id': self.env.uid
        }
        return action

    def create_new_history(self, old_state, new_state):
        for rec in self:
            rec.env['test_app.history'].create({
                'user_id': rec.env.uid,
                'course_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'description': 'A user ' + str(rec.env.user.name) + ' changed the course ' + str(
                    rec.name) + ' from ' + old_state + ' to ' + new_state
            })

    def open_related_responsible_button(self):
        action = self.env['ir.actions.actions']._for_xml_id('base.action_res_users')  # call a user action
        view_id = self.env.ref('base.view_users_form').id  # get a user form view id
        action['res_id'] = self.responsible_id.id  # custom user that open
        action['views'] = [[view_id, 'form']]  # custom open form view because default is list
        return action

    _sql_constraints = [
        (
            "name_description_check",
            "CHECK(name != description)",
            "The title should not be as the description"
        ),
        (
            "name_unique",
            "UNIQUE(name)",
            "This name has been used before"
        )
    ]


class Session(models.Model):
    _name = 'test_app.session'
    _description = 'test_app.session'

    name = fields.Char(required=True)
    ref = fields.Char(default="New", readonly=1)
    start_date = fields.Date("Start Date", default=fields.Date.today())
    duration = fields.Float(digits=(6, 2), help="duration in days")
    seats = fields.Integer(help="number of seats")
    end_date = fields.Date("End Date", store=True, compute="_get_end_date", inverse="_set_end_date")
    instructor_id = fields.Many2one("res.partner", string="Instructor")
    course_id = fields.Many2one("test_app.course", ondelete="cascade", string="Course", required=True)
    course_description = fields.Text(related="course_id.description")  # related field to course model
    attendee_ids = fields.Many2many("res.partner", string="Attendees")
    color = fields.Integer()
    # Dependence Field
    attendance_rate = fields.Float("Attendance rate", compute="_compute_attendance_rate")
    attendee_count = fields.Integer("Attendees Count", compute="_set_attendee_count", store=True)
    active = fields.Boolean("Active", default=True)

    def session_search(self):
        action = self.env.ref('test_app.launch_session_search_wizard').read()[0]
        return action

    @api.constrains("attendee_ids", "instructor_id")
    def _check_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id in record.attendee_ids:
                raise exceptions.ValidationError(_("A session instructor cannot be attendee"))

    @api.depends("seats", "attendee_ids")
    def _compute_attendance_rate(self):
        for record in self:
            if not record.seats:
                record.attendance_rate = 0.0
            else:
                record.attendance_rate = len(record.attendee_ids) / record.seats * 100

    @api.depends("attendee_ids")
    def _set_attendee_count(self):
        for record in self:
            record.attendee_count = len(record.attendee_ids)

    # end_date depend function
    @api.depends("start_date", "duration")
    def _get_end_date(self):
        for record in self:
            if not (record.start_date and record.duration):
                record.end_date = record.start_date
                continue
            # add duration to start_date to get end_date but for example if add Monday+5 get Saturday,
            #   but the end day should be Friday so end_day = start_day + duration - 1
            else:
                duration = timedelta(record.duration, seconds=-1)
                record.end_date = record.start_date + duration

    # end_date reverse function
    @api.depends("start_date", "end_date")
    def _set_end_date(self):
        for record in self:
            if not (record.start_date and record.duration):
                continue
            # compute the difference between dates but for example if sub Friday - Monday = 4,
            #     but the sub between days should be 5 so duration = start_day - end_date + 1
            else:
                record.duration = (record.end_date - record.start_date).days + 1

    @api.onchange("seats", "attendee_ids")
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _('Incorrect seats value'),
                    'message': _('The number of seats may not be Positive')
                }
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _('Too many attendees'),
                    'message': _('Please, increase seats or remove excess attendees')
                }
            }

    @api.model
    def create(self, vals):
        res = super(Session, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('session_seq')
        return res


class Partner(models.Model):
    _inherit = "res.partner"

    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many("test_app.session", string="Sessions", readonly=True)
    # Compute Field
    code = fields.Char("Code", compute="_compute_code")

    def _compute_code(self):
        for record in self:
            record.code = str(random.randint(1, 1e6))


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    related_course = fields.Many2one('test_app.course')
    # parent_id = fields.Many2one('hr.employee', 'Manager', check_company=False)


class CourseHistory(models.Model):
    _name = 'test_app.history'
    _description = 'course state history'

    user_id = fields.Many2one('res.users', string="User")
    course_id = fields.Many2one('test_app.course', string="Course")
    old_state = fields.Selection([('opened', 'Opened'), ('closed', 'Closed')])
    new_state = fields.Selection([('opened', 'Opened'), ('closed', 'Closed')])
    description = fields.Char()
