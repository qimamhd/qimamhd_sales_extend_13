from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class inherit_sales_mans(models.Model):
    _inherit = 'custom.sales.mans'

    branch_id = fields.Many2one('custom.branches', required=True, string="الفرع", default=lambda self: self.env.user.branch_id.id)

    sale_user = fields.Many2one('res.users', string='مستخدم المبيعات', index=True, track_visibility='onchange',
                                  track_sequence=2)