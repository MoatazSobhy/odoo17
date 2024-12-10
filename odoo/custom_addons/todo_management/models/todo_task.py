from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'New Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(tracking=1)
    assign_to = fields.Many2one('res.partner', tracking=1)
    status = fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ], default='new')

    def action_new(self):
        for rec in self:
            rec.status = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.status = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.status = 'completed'

