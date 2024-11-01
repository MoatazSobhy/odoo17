from odoo import models, fields

class Tag(models.Model):
    _name = 'tag'

    name = fields.Char(required=1, default='Tag ',)

    _sql_constraints = [
        ('unique_name','unique("name")','This tag name is exist!'),
    ]