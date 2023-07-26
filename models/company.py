
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class intermediate_sale_man_account(models.Model):
    _inherit = 'res.company'

    intermediate_sale_man_account_id = fields.Many2one('account.account',string="حساب اقفال الدفع للمندوبين ",)