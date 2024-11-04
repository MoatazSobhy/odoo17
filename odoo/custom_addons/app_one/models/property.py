from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'

    name = fields.Char(required=1, default='Property ', size=20)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(required=1)
    expected_price = fields.Float()
    # selling_price = fields.Float(digits=(0,4))
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),
    ], default='north')
    owner_id = fields.Many2one('owner')  # database relation
    tag_ids = fields.Many2many('tag')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!'),
    ]

    # input validation
    @api.constrains('bedrooms')
    # self represents record or record set
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                # print("Bedrooms not valid")
                raise ValidationError("Please add valid number of bedrooms!")

    @api.constrains('selling_price')
    def _check_selling_price_greater_zero(self):
        for rec in self:
            if rec.selling_price == 0.00:
                # print("Selling price is not valid")
                raise ValidationError("Please add valid selling price!")

    def action_draft(self):
        for rec in self:
            rec.state = "draft"
            # self.write({
            #     'state':'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.state = "pending"
            # self.write({
            #     'state':'pending'
            # })

    def action_sold(self):
        for rec in self:
            rec.state = "sold"
            # self.write({
            #     'state':'sold'
            # })


    # # Create Method Overwrite
    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals)
    #     print("Inside Create Method")
    #     # logic
    #     return res
    #
    # # Read Method Overwrite
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("Inside Update (_search) Method")
    #     #logic
    #     return res
    #
    # # Write Method Overwrite
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("Inside Write Method")
    #     #logic
    #     return res
    #
    # # Delete Method Overwrite
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("Inside Delete (unlink) Method")
    #     #logic
    #     return res