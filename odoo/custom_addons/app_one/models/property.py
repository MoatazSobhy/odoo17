from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

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
    # garage = fields.Boolean(groups="app_one.property_manager_group")
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
    active = fields.Boolean(default=True)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    create_time = fields.Datetime(default=fields.Datetime.now())   # just to test default time
    next_time = fields.Datetime(compute='_compute_next_time')      # just to test default time

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
            rec.create_history_record(rec.state, "draft")
            rec.state = "draft"
            # self.write({
            #     'state':'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, "pending")
            rec.state = "pending"
            # self.write({
            #     'state':'pending'
            # })

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, "sold")
            rec.state = "sold"
            # self.write({
            #     'state':'sold'
            # })

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, "closed")
            rec.state = "closed"
            # self.write({
            #     'state':'closed'
            # })

    # method for change state wizard
    def action_open_change_state(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_action')
        action['context'] = {'default_property_id': self.id}
        return action
                
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
        print(self.env['property'].search([('name', '=', 'Property 1')]))
        print(self.env['property'].search([('&', 'name', '=', 'Property 1'), ('selling_price', '=', '1000')]))
        print(self.env['property'].search([('|', 'name', '=', 'Property 1'), ('selling_price', '=', '1000')]))
        print(self.env['property'].search([('!', 'name', '=', 'Property 1'), ('selling_price', '=', '1000')]))
        # we also can use update (write)
        # we also can use unlink (delete)

    # Create Method Overwrite
    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
          rec.env['property.history'].create({
              'user_id': rec.env.uid,
              'property_id': rec.id,
              'old_state': old_state,
              'new_state': new_state,
              'reason': reason,
              'line_ids': [(0, 0, {'description': line.description,'area': line.area}) for line in rec.line_ids],
          })

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False

    # method for smart button
    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

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


