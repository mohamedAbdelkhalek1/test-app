from odoo import models, fields


class SessionSearch(models.TransientModel):
    _name = 'session.search'
    _description = 'session search with wizard'

    start_date = fields.Date("From")
    end_date = fields.Date("To")

    def session_search_action(self):
        action = self.env.ref('test_app.session_search_action').read()[0]
        action['context'] = {'start': self.start_date, 'end': self.end_date}
        return action
