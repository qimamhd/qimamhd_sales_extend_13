# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import datetime



class xx_account_move(models.Model):
    _inherit = 'account.move'

    sale_man_payment_id = fields.Many2one('saleman.payment', copy=False,string="رقم الدفع للمندوبين")

    def unlink(self):
        for rec in self:
            if rec.type == 'entry':
                if rec.sale_man_payment_id:
                    rec.sale_man_payment_id.write({'account_move_id': False})
                    rec.write({'sale_man_payment_id': False})
        return super(xx_account_move, self).unlink()





class pl_closed(models.Model):
    _name = 'saleman.payment'
    _inherit = ['mail.thread']

    _rec_name = 'id'
    seq = fields.Integer(
        string='رقم العملية',
        copy=False,
        readonly=True,
        default=lambda self: self._get_sequence(),)

    def _get_sequence(self):
        # print(self.env.context.get('report_name', False))
        branch_id = self.env.user.branch_id.id
        if branch_id:
            sql_query = "select max(COALESCE(seq,0)) as seq from saleman_payment where branch_id=%s" % (branch_id)


            self.env.cr.execute(sql_query)
            seq = self.env.cr.fetchone()
            x = seq[0]
            if x:
                x = x + 1
                return (x)
            else:
                x = 1
                return (x)

    order_date = fields.Date(string="تاريخ الدفع", required=True, default=fields.Date.today,copy=False)

    branch_id = fields.Many2one('custom.branches', string='الفرع', readonly=True, copy=False,
                                default=lambda self: self.env.user.branch_id.id)
    sales_man_id = fields.Many2one('custom.sales.mans', string='مندوب المبيعات', required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, readonly=True,string="الشركة")

    account_id = fields.Many2one('account.account',required=True,string="حساب اقفال الصرف للمندوبين")
    journal_id = fields.Many2one('account.journal', required=True, string="الصندوق / البنك",
                                             domain="[('type','in', ['cash','bank']),('branch_id','=',branch_id)]")
    description = fields.Char(string="الوصف")
    posted_flag = fields.Boolean(string="تم الترحيل")

    amount = fields.Float(string="المبلغ", required=True,copy=False)
    account_move_id = fields.Many2one('account.move',copy=False)

    post_payment_flag = fields.Boolean(default=lambda self: self._default_post_payment_flag(),
                                            compute="_get_post_payment_flag")
    source_move_id = fields.Many2one('account.move',copy=False)
    source_so_id = fields.Many2one('sale.order',copy=False)

    # @api.depends('company_id')
    def _get_post_payment_flag(self):
        params = self.env['ir.config_parameter'].sudo()
        l_post_sale_man_payment = params.get_param('post_sale_man_payment',
                                               default=False)
        print("l_post_sale_man_payment", l_post_sale_man_payment)

        for rec in self:
            rec.post_payment_flag = l_post_sale_man_payment

    def _default_post_payment_flag(self):
        params = self.env['ir.config_parameter'].sudo()
        l_post_sale_man_payment = params.get_param('post_sale_man_payment',
                                               default=False)
        print("l_post_sale_man_payment", l_post_sale_man_payment)

        return l_post_sale_man_payment

    user_id = fields.Many2one(
        'res.users', string='مدخل البيانات/مسئول المبيعات', readonly=True, copy=False,
        required=True, default=lambda self: self.env.uid)

    # def _default_sale_man(self):
    #
    #     active_ids = self._context.get('active_ids', [])
    #     sale_man_id={}
    #     print("self.source_payment",self.source_payment)
    #     if self.source_payment == 'so':
    #         so = self.env['sale.order'].search([('id', '=', active_ids)])
    #         sale_man_id =  so.sales_man_id
    #     else:
    #         move = self.env['account.move'].search([('id', '=', active_ids)])
    #         sale_man_id =  move.sales_man_id
    #
    #
    #     return sale_man_id
    @api.onchange('company_id')
    def _default_intermdiate_account_sale_man(self):
        print("elf.company_id.intermediate_sale_man_account_id",self.company_id.intermediate_sale_man_account_id)
        self.account_id =  self.company_id.intermediate_sale_man_account_id.id

    def confirm_payment(self):
        for rec in self:

            # check_close = self.env['cash.close.closed'].search([('branch_id','=', rec.branch_id.id),('order_date','=', rec.order_date)])
            if rec.sales_man_id and rec.journal_id and rec.amount and rec.account_id:
                    line_ids = []

                    if not rec.account_move_id:
                            credit_vals = (0, 0, {
                                'name': rec.sales_man_id.name,
                                'amount_currency': 0.0,

                                'company_currency_id': rec.company_id.currency_id.id,
                                'debit': 0.0,
                                'credit': rec.amount,
                                # 'balance': payment.local_amount if payment.check_multi_currency else payment.payment_amount,
                                'date': rec.order_date,
                                'date_maturity': rec.order_date,
                                'account_id': rec.journal_id.default_credit_account_id.id,
                                'account_internal_type': rec.account_id.internal_type,
                                # 'parent_state': 'posted',
                                'ref': 'الدفع للمندوب : ' + str(rec.sales_man_id.name) + ' [ '+ str( rec.description) + ' ] ',
                                'journal_id': rec.journal_id.id,
                                'company_id': rec.company_id.id,
                                'quantity': 1,

                            })
                            line_ids.append(credit_vals)

                            debit_vals = (0, 0, {
                                'name': rec.sales_man_id.name,
                                'amount_currency': 0.0,

                                'company_currency_id':rec.company_id.currency_id.id,
                                'debit': rec.amount,
                                'credit': 0.0,
                                # 'balance': -(line.l_local_amount) if payment.check_multi_currency else -(line.l_payment_amount),
                                'date': rec.order_date,
                                'date_maturity': rec.order_date,
                                'account_id': rec.account_id.id,
                                'account_internal_type': rec.account_id.internal_type,
                                # 'parent_state': 'posted',
                                'ref': 'الدفع للمندوب : ' + str(rec.sales_man_id.name) + ' [ '+ str( rec.description) + ' ] ',
                                'journal_id': rec.journal_id.id,
                                'company_id':rec.company_id.id,
                                'quantity': 1,

                            })

                            line_ids.append(debit_vals, )
                    if line_ids:
                        ref = 'الدفع للمندوب : ' + str(rec.sales_man_id.name) + ' [ ' + str(rec.description) + ' ] ',
                        mov_vals = {
                            'date': rec.order_date,
                            'ref': ref,
                            # 'state': 'posted',
                            'type': 'entry',
                            'journal_id': rec.journal_id.id,
                            'company_id': rec.company_id.id,
                            'currency_id': rec.company_id.currency_id.id,
                            'sale_man_payment_id': rec.id,
                            # 'amount_total': payment.payment_amount, #if payment.check_multi_currency and (payment.company_id.currency_id.id != line.currency_id.id) else payment.local_amount,
                            # 'amount_total_signed': payment.local_amount, #if payment.check_multi_currency and (payment.company_id.currency_id.id != line.currency_id.id) else payment.local_amount,
                            'invoice_user_id': self.env.uid,
                            'line_ids': line_ids,
                        }

                        print(mov_vals)
                        entry_moves = self.env['account.move'].create(mov_vals)
                        rec.write({'account_move_id':entry_moves.id})
                        rec.write({'posted_flag': True })
                        if rec.post_payment_flag:
                            entry_moves.post()

                        print("entry_moves", entry_moves)
                    else:
                        raise ValidationError(
                            "تنبيه .. تم احتساب الصرف مسبقا  وانشاء القيد برقم [%s] " % rec.account_move_id.name)
            else:

                raise ValidationError(
                    "تنبيه .. لا يمكن الاستمرار توجد بينات غير مكتملة ")


    def un_confirm_payment(self):
        for rec in self:
            if rec.account_move_id:
                rec.account_move_id.unlink()

    def call_entry(self):
        for rec in self:
            action = self.env.ref('account.action_move_journal_line')
            result = action.read()[0]
            result.pop('id', None)
            result['context'] = {}
            result['domain'] = [('sale_man_payment_id', '=', rec.id), ('type', '=', 'entry')
                                ]
            return result
