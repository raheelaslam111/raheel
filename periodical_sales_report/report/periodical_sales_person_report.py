# -*- coding: utf-8 -*-

from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime



class ReportPeriodicalSalePerson(models.AbstractModel):
    _name = 'report.periodical_sales_report.report_periodical_sales_person'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        period = data['form']['period']
        state = data['form']['state']
        sale_person = data['form']['sale_person_id']
        sale_person_id = self.env['res.users'].search([('id', '=', int(sale_person))], limit=1)
        total_sale = 0.0
        period_value = ''

        if date_from and date_to:
            domain = [('date_order', '>=', date_from),
                      ('date_order', '<=', date_to),
                      ('user_id', '=', sale_person_id.id)]
        else:
            if period == 'today':
                domain = [('date_order', '>=', datetime.datetime.now()
                           .strftime('%Y-%m-%d 00:00:00')),('date_order',
                            '<=', datetime.datetime.now()
                            .strftime('%Y-%m-%d 23:59:59')),
                          ('user_id', '=', sale_person_id.id)]
                period_value = 'Today'
            elif period == 'last_week':
                domain = [('date_order', '>=', (datetime.date.today()
                -datetime.timedelta(days=7)).strftime('%Y-%m-%d 00:00:00')),
                 ('date_order', '<=', datetime.datetime.now()
                  .strftime('%Y-%m-%d 23:59:59'),
                  ('user_id', '=', sale_person_id.id))
                ]
                period_value = 'Last Week'
            elif period == 'last_month':
                domain = [
                    ('date_order', '>=',
                     (datetime.date.today() - relativedelta(months=1)).
                     strftime('%Y-%m-%d 00:00:00')),
                    ('date_order', '<=',
                     datetime.datetime.now().strftime('%Y-%m-%d 23:59:59')),
                    ('user_id', '=', sale_person_id.id)
                ]
                period_value = 'Last Month'
        if state != 'all':
            domain.append(('state','=',state))

        sale_orders_lines = []
        orders = self.env['sale.order'].search(domain)
        data_dict = {}
        for order in orders:
            for line in order.order_line:
                # existing_line = sale_orders_lines.filtered(lambda r: not r.product_id == line.product_id.id)
                # print(existing_line,'before')
                key = (line.product_id.id)
                if key in data_dict:
                    values = {
                        'product_uom_qty': data_dict[key].get('product_uom_qty')+line.product_uom_qty,
                        'price_subtotal': data_dict[key].get('price_subtotal')+line.price_subtotal,
                    }
                    data_dict[key].update(values)
                else:
                    data_dict[key] = {
                        'product_id': line.product_id.id,
                        'product': line.product_id.name,
                        'product_uom_qty': line.product_uom_qty,
                        'price_subtotal' : line.price_subtotal,
                    }
                # sale_orders_lines.append([0,0,values])
            total_sale += order.amount_total

        # data = {}
        # self.search([]).unlink()
        # mrp_productions = self._context.get('active_ids')
        # mrp_production = self.env['mrp.production'].browse(mrp_productions)
        # products_without_default_code = mrp_production.mapped('move_raw_ids').filtered(
        #     lambda x: not x.product_id.default_code
        # )
        #
        # raws = mrp_production.mapped('move_raw_ids').sorted(
        #     key=lambda r: r.product_id.default_code
        # )
        #
        # for r in raws:
        #     key = (r.product_id.id, r.raw_material_production_id.id)
        #     if key not in data:
        #         data[key] = {
        #             'product_id': r.product_id.id,
        #             'code': r.product_id.default_code,
        #             'total_qty': r.product_id.qty_available,
        #             'virtual_qty': r.product_id.virtual_available,
        #             'origin': r.reference,
        #             'production_id': r.raw_material_production_id.id,
        #         }
        #     else:
        #         data[key].update({
        #             'total_qty': data[key].get('total_qty') + r.product_id.qty_available,
        #         })
        for vals in data_dict:
            # print('vals',data_dict[vals])
            sale_orders_lines.append(data_dict[vals])
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'period' : period_value,
            'date_from': date_from,
            'date_to': date_to,
            'sale_orders_lines' : sale_orders_lines,
            'total_sale' : total_sale,
            'sale_person_id': sale_person_id,
        }