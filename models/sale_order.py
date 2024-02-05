# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class set_sale_order(models.Model):
    _inherit = 'sale.order'
    
    partner_mobile = fields.Char(string="رقم الجوال")

    @api.onchange('partner_id')
    def get_partner_mobile(self):
        for rec in self:
            if rec.partner_id:
                rec.write({'partner_mobile': rec.partner_id.mobile})

    @api.constrains('partner_mobile')
    def set_partner_mobile(self):
        if self.partner_mobile:
            self.partner_id.write({'mobile': self.partner_mobile})
            
        
    def _prepare_invoice(self):
        invoice_vals = super(set_sale_order, self)._prepare_invoice()
        check_partner_mobile_field = self.env['ir.model.fields'].search([('model','=','account.move'),('name','=','partner_mobile')])
        if check_partner_mobile_field:
            invoice_vals.update({'partner_mobile': self.partner_mobile or False})

        return invoice_vals



    
