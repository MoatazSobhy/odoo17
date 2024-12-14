from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Building(models.Model):
    _name = 'building'
    _description = 'New Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    #_rec_name = 'code'  # default is name if exist

    name = fields.Char(required=1, tracking=1, default='Building ')
    number = fields.Integer(required=1, tracking=1)
    code = fields.Char(required=1, tracking=1)
    description = fields.Text(required=1, tracking=1)
    active = fields.Boolean(default=True)          # to be able to archive

    # this is more from me
    @api.constrains('number')
    def _check_number_greater_than_zero(self):
        for rec in self:
            if rec.number <= 0:
                raise ValidationError("Building number must be more than zero!")