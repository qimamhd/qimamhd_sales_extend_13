from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class inherit_sale_custom_fields(models.Model):
    _inherit = 'sale.order.line'

    product_serial_no = fields.Char(string="الرقم التسلسلي")

    def _prepare_invoice_line(self):
        # res = super(SaleOrderLine, self)._prepare_invoice_line(qty)odoo13
        res = super(inherit_sale_custom_fields, self)._prepare_invoice_line()
        res.update({'product_serial_no': self.product_serial_no or False })

        return res


class inherit_account_custom_fields(models.Model):
    _inherit = 'account.move.line'

    product_serial_no = fields.Char(string="الرقم التسلسلي")

