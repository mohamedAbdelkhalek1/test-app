from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = "test_app.wizard"
    _description = "Wizard: quick registration to Attendees"

    def _default_sessions(self):
        return self.env['test_app.session'].browse(self._context.get('active_id'))

    session_ids = fields.Many2one("test_app.session", string="Session", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many("res.partner", string="Attendees")

    def action_register_attendees(self):
        self.session_ids.attendee_ids |= self.attendee_ids
