from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_ids = fields.Many2one('property')
    price = fields.Float(related="property_ids.selling_price")
    # price = fields.Float(compute="_compute_price", store=1)

    # @api.depends('price','property_ids')
    # def _compute_price(self):
    #     for rec in self:
    #         rec.price = rec.property_ids.selling_price


