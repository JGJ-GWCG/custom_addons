from odoo import models, fields

class LoanModel(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char( string = 'Application Number', required=True)
    currency_id = fields.Many2one(string = 'Currency', required=True, comodel_name='res.currency')
    date_application = fields.Date( string = 'Application Date')
    date_approval = fields.Date( string = 'Approval Date')
    date_rejection = fields.Date( string = 'Rejection Date')
    date_signed = fields.Datetime( string = 'Signed on')
    down_payment = fields.Monetary( string = 'Downpayment', currency_field='currency_id') #Relación con el campo de currency_id
    interest_rate = fields.Float( string = 'Interest Rate (%)', digits = (5,4))
    loan_amount = fields.Monetary( string = 'Loan Amount', currency_field='currency_id') #Relación con el campo de currency_id
    loan_term = fields.Integer( string = 'Loan Term (Months)', required = True, default = 36)
    rejection_reason = fields.Text( string = 'Rejection Reason')
    state = fields.Selection (string = 'Status', selection=[('draft', 'Draft'), ('sent', 'Sent'), ('review', 'Credit Check'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('signed', 'Signed'), ('cancel', 'Canceled')], default='draft')
    notes = fields.Html (string = "Notes")