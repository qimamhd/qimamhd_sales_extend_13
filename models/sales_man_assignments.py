# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from odoo.exceptions import ValidationError
from datetime import datetime

class xx_sales_man_assignments(models.Model):
    _name = 'wo.salesman.assignments'
    _description = 'wo salesman assignments'

    _rec_name = "salesman_id"

    salesman_id = fields.Many2one('custom.sales.mans', required=True,string="المندوب",domain=[('sale_man_type','=', 'internal')])
    assign_date = fields.Date(string="تاريخ الاسناد", required=True, default=fields.Date.today,copy=False)
    close_date = fields.Date(string="تاريخ الايقاف", copy=False,readonly=True)

    branch_id = fields.Many2one('custom.branches', string='الفرع المسند اليه', copy=False,required=True,)
    state = fields.Selection([('current','متوفر لدى الفرع'),('closed','ايقاف')],string="الحالة", default='current',readonly=True)


    @api.model
    def create(self, vals_list):
        print("vals_list", vals_list)
        salesman_id = vals_list.get('salesman_id')
        assign_date = vals_list.get('assign_date')
        salesman_assign = self.env['wo.salesman.assignments'].search([('salesman_id','=',salesman_id),('state','=', 'current')])
        for line in salesman_assign:
            line.write({'close_date': assign_date,
                        'state': 'closed'})
        res = super(xx_sales_man_assignments, self).create(vals_list)

        return res

    def unlink(self):
        for rec in self:
            raise ValidationError(
                "تنبيه .. لا يمكن الحذف   ")
        return super(xx_sales_man_assignments, self).unlink()


    @api.constrains('salesman_id','state','branch_id')
    def change_user_branch(self):
        for rec in self:
            if rec.state == 'current':
                if rec.salesman_id.sale_user:
                    rec.salesman_id.sale_user.update({'branch_id': rec.branch_id.id})
                    rec.salesman_id.sale_user.write({'allowed_branch_ids': [(4, rec.branch_id.id)]})
