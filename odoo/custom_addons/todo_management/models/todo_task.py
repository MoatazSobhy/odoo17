from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'New Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, tracking=1)
    description = fields.Text(required=1, tracking=1)
    due_date = fields.Date(required=1, tracking=1)
    assign_to = fields.Many2one('res.partner', tracking=1)
    status = fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('closed','Closed'),
        ], default='new', tracking=1)
    estimated_time = fields.Integer(required=1, tracking=1)
    line_ids = fields.One2many('todo.task.line', 'todo_task_id')
    is_late = fields.Boolean()
    active = fields.Boolean(default=True)

    def action_new(self):
        for rec in self:
            rec.status = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.status = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.status = 'completed'

    def action_closed(self):
        for rec in self:
            rec.status = 'closed'

    @api.constrains('line_ids', 'estimated_time')
    def _check_lines_sum_time(self):
        for rec in self:
            total_time = sum(rec.line_ids.mapped('time'))
            if total_time > rec.estimated_time:
                raise ValidationError("Your time sheet times must not exceed the estimated time!")

    def check_due_date(self):
        todo_task_ids = self.search([])
        for rec in todo_task_ids:
            if rec.due_date and rec.status != 'completed' and rec.due_date < fields.date.today():
                rec.is_late = True
            else:
                rec.is_late = False

class TodoTaskLine(models.Model):
    _name = 'todo.task.line'

    todo_task_id = fields.Many2one('todo.task')
    date = fields.Date(required=1)
    description = fields.Char(required=1, default='Do ', size=20)
    time = fields.Integer(required=1)

    @api.constrains('time')
    def _check_time_greater_zero(self):
        for rec in self:
            if rec.time == 0:
                raise ValidationError("Please add suitable time!")

