# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import pdb

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError, ValidationError



class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_second2 = fields.Float(string='Discount%', default=0.0)
    total_custom_discount = fields.Float(string='Extra Discount',compute='calc_extra_discount')
    lines_total_discount = fields.Float(string='Discount',compute='calc_lines_total_discount')
    positive_total_amount = fields.Float(string='Discount',compute='calc_lines_total_discount')


    @api.onchange('order_line')
    def assign_sequence_to_order_line(self):
        index = 0
        for line in self.order_line:
            line.custom_sequence = index + 1
            index += 1



    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        required_line = self.order_line.filtered(lambda m: m.product_id.qty_available < m.product_uom_qty and m.product_id.name!='Discount')
        if required_line:
            raise ValidationError(_('Product is no longer available You can not proceed.'))
        return res

    @api.model
    def create(self,vals):
        res = super(SaleOrder, self).create(vals)
        required_line = res.order_line.filtered(lambda m: m.product_id.qty_available < m.product_uom_qty and m.product_id.name!='Discount')
        if required_line:
            raise ValidationError(_('Product is no longer available You can not proceed.'))
        return res

    @api.depends('order_line')
    def calc_lines_total_discount(self):
        for rec in self:
            # percentage_discount_amount = 0.0
            positive_amount = 0.0
            lines_discount_total = 0.0


            # for line in rec.order_line.filtered(lambda b: b.price_subtotal>0):
            #     percentage_discount_amount += line.discount

                # product*quantity   it is the sum of discount of all lines
            for line in rec.order_line.filtered(lambda b: b.price_subtotal > 0 and b.product_id.name != 'Discount'):
                lines_discount_total += ((line.price_unit*line.product_uom_qty)/100)*line.discount

             # Positive amount
            for line in rec.order_line.filtered(lambda b: b.price_subtotal>0):
                positive_amount += line.price_unit*line.product_uom_qty


            rec.positive_total_amount = positive_amount
            rec.lines_total_discount = lines_discount_total


    def calc_extra_discount(self):
        for rec in self:
            total = sum(rec.order_line.filtered(lambda b: b.is_custom_discount == True).mapped('price_unit'))
            rec.total_custom_discount = total

    def add_discount_line_in_so(self):
        discount=0
        if self.amount_total > 0 and self.discount_second2>0:
            discount = (self.amount_total/100)*self.discount_second2
        product = self.env['product.product'].search([('name','=','Discount')],limit=1)
        sequence_list = []
        for line in self.order_line:
            sequence_list.append(line.sequence)
        max_seq = max(sequence_list)
        if not product:
            product_vals = {
                'name':'Discount',
                'sale_ok':'True',
                'purchase_ok':'True',
                'lst_price':0.0,
            }
            product = self.env['product.product'].create(product_vals)
        values = {
            'product_id':product.id,
            'sequence': max_seq + 1,
            'price_unit':-discount,
            'is_custom_discount': True,
            'order_id': self.id,

        }
        order_line = self.env['sale.order.line'].create(values)




class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_custom_discount = fields.Boolean('Is Custom Discount',default=False)
    custom_sequence = fields.Integer(readonly=True,string='S.NO')

    # @api.depends('sequence')
    # def get_sequence_from_sequence(self):
    #     for rec in self:
    #         rec.for_compute = 'abc'
            # index = 0
            # for line in rec.order_id.order_line:
            #     line.custom_sequence = index+1
            #     index += 1
            # rec.custom_sequence = rec.sequence


    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        len_of_lines = len(res.order_id.order_line)
        res.custom_sequence = len_of_lines
        return res

#
#     @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','discount_second2')
#     def _compute_amount(self):
#         """
#         Compute the amounts of the SO line.
#         """
#         for line in self:
#             price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
#             taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
#                                             product=line.product_id, partner=line.order_id.partner_shipping_id)
#             line.update({
#                 'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
#                 'price_total': taxes['total_included']-line.discount_second2,
#                 'price_subtotal': taxes['total_excluded']-line.discount_second2,
#             })
#             if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
#                     'account.group_account_manager'):
#                 line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange('order_line')
    def assign_sequence_to_order_line(self):
        index = 0
        for line in self.order_line:
            line.custom_sequence = index + 1
            index += 1


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    custom_sequence = fields.Integer(readonly=True,string='S.NO')

    @api.model
    def create(self, vals):
        res = super(PurchaseOrderLine, self).create(vals)
        len_of_lines = len(res.order_id.order_line)
        res.custom_sequence = len_of_lines
        return res

    # def write(self, vals):
    #     res = super(PurchaseOrderLine, self).write(vals)
    #     index = 0
    #     for line in self.order_id.order_line:
    #         line.custom_sequence = index+1
    #         index += 1
    #     return res







