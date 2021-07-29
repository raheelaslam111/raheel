# -*- coding: utf-8 -*-
import pdb

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date



class PettyCashRequest(models.Model):
    _name = "petty.cash.request"
    _description = "petty cash request"

    reference = fields.Char(string='Reference')
    partner_id = fields.Many2one('res.partner', string='Requester')
    petty_cash_holder_id = fields.Many2one('petty.cash.holder',string="Petty Cash Holder")
    requested_on = fields.Date(string='Requested On')
    approved_on = fields.Date(string='Approved On')
    # 'Select From Dropdown List  form Project BOQ's Module (Only Active Projects)'
    project_id = fields.Many2one('project.project')
    cash_request_line_ids = fields.One2many('cash.request.line','petty_cash_request_id',string='Cash Request Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled')
    ], string='State', readonly=True)

    # @api.model
    # def create(self,vals):
    #
    #     res = super(PettyCashRequest, self).create(vals)

    def action_approve(self):
        self.approved_on = fields.date.today()
        print()
        sequence = self.env['ir.sequence'].search([(
            'code', '=', 'Pettyrequest',
        )], limit=1)
        sequence.write({'number_next_actual': 1000})
        self.reference = self.env['ir.sequence'].next_by_code('Pettyrequest') or _('New')
        self.state='approved'

    def action_cancel(self):
        self.state='cancel'

    def action_reset(self):
        self.state='draft'

    def action_create_payment(self):
        y=0

    def action_create_bill(self):
        y=0

class CashRequestLine(models.Model):
    _name = "cash.request.line"
    _description = "petty cash request line"

    amount_requested = fields.Float(string="Amount Requested")
    amount_approved = fields.Float(string="Amount Approved")
    amount_paid = fields.Float(string="Amount Paid")
    balance_amount = fields.Float(string="Balance Amount")
    petty_cash_request_id = fields.Many2one('petty.cash.request',string='Petty Cash Request')

class PettyCashHolder(models.Model):
    _name = "petty.cash.holder"
    _description = "petty cash holder"


    partner_id = fields.Many2one('res.partner', string='Partner')
    journal_id = fields.Many2one('account.journal',string='Journal')
    approved_cash_limit = fields.Float(string="Approved Cash Limit")
    cash_onhand = fields.Float(string="Cash on Hand",help="Approved Cash - Cash Disbursed")

    # def unlink(self):
    #     # Will be allowed if no request / Payment is linked with Petty Cash Holder From



class AccountMove(models.Model):
    _inherit = "account.move"

    petty_cash_request_id = fields.Many2one('petty.cash.request',string='Petty Cash Request')