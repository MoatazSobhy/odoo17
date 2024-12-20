from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'New Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='New', readonly=1)
    name = fields.Char(required=1, default='Property ', size=20)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(required=1, tracking=1)
    expected_price = fields.Float(tracking=1)
    # selling_price = fields.Float(digits=(0,4))
    selling_price = fields.Float(tracking=1)
    # diff = fields.Float(compute='_compute_diff', store=1, readonly=0)
    diff = fields.Float(compute='_compute_diff', store=1)
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
    owner_phone = fields.Char(related='owner_id.phone', readonly=0, store=1)
    owner_address = fields.Char(related='owner_id.address', readonly=0, store=1)
    tag_ids = fields.Many2many('tag')
    line_ids = fields.One2many('property.line','property_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()

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

    def action_closed(self):
        for rec in self:
            rec.state = "closed"
            # self.write({
            #     'state':'closed'
            # })

    # can depend on views fields or model fields or relational fields
    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print("inside _compute_diff method")
            rec.diff = rec.expected_price - rec.selling_price

    # can depend on views fields only that appears in form view (simple fields names)
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print("inside _onchange_expected_price method")
            if rec.expected_price < 0.00:
                return {
                    'warning' : {'title': 'warning', 'message': 'negative number!', 'type': 'notification'}
                }
            # if rec.expected_price < 0.00:
            #     raise ValidationError('Expected price can not be less than zero!')

    # This is more to not exceed the number of bedrooms
    @api.constrains('line_ids', 'bedrooms')
    def _check_max_lines(self):
        for rec in self:
            if len(rec.line_ids) > rec.bedrooms:
                raise ValidationError(f"You have only {rec.bedrooms} bedrooms.")

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.state != 'sold' and rec.expected_selling_date < fields.date.today():
                rec.is_late = True
            else:
                rec.is_late = False

    def action(self):
        print(self.env)
        print(self.env.user.name)
        print(self.env.user.login)
        print(self.env.user.id)
        print(self.env.uid)
        print(self.env.company.name)
        print(self.env.company.id)
        print(self.env.company.street)
        print(self.env.context)
        print(self.env.cr)
        print(self.env['owner'].create({
            'name': 'Name One',
            'phone': '01203139628',
            'address': 'Alexandria',
        }))
        print(self.env['owner'].create({
            'name': 'Name Two',
            'phone': '01208346606',
            'address': 'Cairo',
        }))
        print(self.env['owner'].search([]))
        # we also can use update (write)
        # we also can use unlink (delete)

    # Create Method Overwrite
    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

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
    #     print("Inside Read (_search) Method")
    #     #logic
    #     return res
    #
    # # Write Method Overwrite
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("Inside Write (update) Method")
    #     #logic
    #     return res
    #
    # # Delete Method Overwrite
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("Inside Delete (unlink) Method")
    #     #logic
    #     return res


class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char(required=1, default='Bedroom ', size=20)


