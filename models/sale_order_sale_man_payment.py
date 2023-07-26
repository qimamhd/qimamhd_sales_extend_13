# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class set1_partner_types(models.Model):
    _inherit = 'sale.order'

    sale_man_payment_count = fields.Integer(compute="get_sale_man_payment_count")

    # ===========================================================================================

    def action_register_sale_man_payment(self):
        # action = self.env.ref('account.view_account_payment_invoice_form')
        # result = action.read()[0]
        # result.pop('id', None)
        # print(self.amount_total)
        # result['context'] = {'default_payment_type': 'inbound','default_partner_type': 'customer',
        #                      'res_partner_search_mode': 'customer','search_default_inbound_filter':1,
        #                      'default_partner_id': self.partner_id.id,'default_amount': self.amount_total,
        #                      'default_communication': self.name}
        # return result
        sale_man_amount = 0.00
        if self.sales_man_id.due_amount_type == 'percentage':
             if self.sales_man_id.due_amount:
               sale_man_amount = self.amount_untaxed * (self.sales_man_id.due_amount /100)
        elif self.sales_man_id.due_amount_type == 'amount':
            if self.sales_man_id.due_amount:
                sale_man_amount = self.sales_man_id.due_amount


        return {
            'name': _('Register Sale Man Payment'),
            'res_model': 'saleman.payment',
            'view_mode': 'form',
            'view_id': self.env.ref(
             'qimamhd_sales_extend_13.saleman_payment_form_view').id,
             'context': {'default_sales_man_id': self.sales_man_id.id, 'default_branch_id':self.branch_id.id,
                              'default_amount': sale_man_amount, 'default_source_so_id': self.id
                              },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    def get_sale_man_payment_count(self):
        for rec in self:
            payment = self.env['saleman.payment'].search([('source_so_id', '=', rec.id)])
            rec.sale_man_payment_count = len(payment)


    def action_sale_man_payment(self):
        for rec in self:

            payment = self.env['saleman.payment'].search([('source_so_id', '=', rec.id)])

            action = self.env.ref('qimamhd_sales_extend_13.action_saleman_payment_view')
            result = action.read()[0]
            result.pop('id', None)
            result['context'] = {}
            result['domain'] = [('id', 'in', payment.ids)]
            return result

    # return {
    #         'name': _('Register Payment'),
    #         'res_model': 'account.payment',
    #         'view_mode': 'tree',
    #         'view_id': self.env.ref(
    #             'account.action_account_payments').id,
    #         'context': {'default_payment_type': 'inbound', 'default_partner_type': 'customer',
    #                     'res_partner_search_mode': 'customer', 'search_default_inbound_filter': 1,
    #                     'default_partner_id': self.partner_id.id, 'default_amount': self.amount_total,
    #                     'default_communication': self.name},
    #         'domain': [('id', 'in', payment.ids)],
    #
    #
    #         'type': 'ir.actions.act_window',
    #     }




