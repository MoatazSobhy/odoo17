from odoo import models, fields
from odoo.exceptions import ValidationError


class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ], default='draft', required=1)
    reason = fields.Char(required=1)

    def action_confirm(self):
        if self.property_id.state == 'closed':
            self.property_id.state = self.state
            self.property_id.create_history_record('closed', self.state, self.reason)
        else:
            raise ValidationError("You can use it to convert closed state only!")
