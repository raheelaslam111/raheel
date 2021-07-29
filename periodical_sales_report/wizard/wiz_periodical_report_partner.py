# -*- coding: utf-8 -*-

from odoo import api, fields, models



class PeriodicalReportWizardPartner(models.TransientModel):
    _name = "periodical.report.wizard.partner"

    period = fields.Selection([
        ('today', 'Today'),
        ('last_week', 'Last Week'),
        ('last_month','Last Month')],
        'Period',
         default='today',
        help="Select the option for priting report for daily, "
             "weekly or monthly")
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('all', 'All')
        ], string='Status',  default='all')
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    sale_person_id = fields.Many2one('res.users',string='Salesperson',required=True)


    # @api.multi
    def check_report(self):
        period = self._fields['period'].get_values(self.env)
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'period' : self.period,
                'state' : self.state,
                'sale_person_id': self.sale_person_id.id,
            },
        }
        return self.env.ref('periodical_sales_report.action_report_periodical_sales_partner').report_action(self, data=data)
