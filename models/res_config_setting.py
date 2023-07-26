
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    # intermediate_sale_man_account_code = fields.Integer()
    post_sale_man_payment = fields.Boolean(string="ترحيل قيد الدفع للمندوبين تلقائيا بعد الاعتماد",)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()

        l_post_sale_man_payment = params.get_param('post_sale_man_payment',  default=False)

        res.update(post_sale_man_payment=l_post_sale_man_payment)

        return res

    def set_values(self):
            super(ResConfigSettings, self).set_values()


            self.env['ir.config_parameter'].sudo().set_param(
                "post_sale_man_payment",
                self.post_sale_man_payment)
