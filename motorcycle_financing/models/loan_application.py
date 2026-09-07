from odoo import models, fields

class LoanModel(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char( string = 'Application Number', required=True)
    currency_id = fields.Many2one(string = 'Currency', required=True, comodel_name='res.currency', default=lambda self:self.env.company.currency_id.id)
    date_application = fields.Date( string = 'Application Date', readonly=True, copy=False)
    date_approval = fields.Date( string = 'Approval Date', readonly=True, copy=False)
    date_rejection = fields.Date( string = 'Rejection Date', readonly=True, copy=False)
    date_signed = fields.Datetime( string = 'Signed on', readonly=True, copy=False)
    down_payment = fields.Monetary( string = 'Downpayment', required=True, currency_field='currency_id') #Relación con el campo de currency_id
    interest_rate = fields.Float( string = 'Interest Rate (%)', required=True, digits = (5,2))
    loan_amount = fields.Monetary( string = 'Loan Amount', required=True, currency_field='currency_id') #Relación con el campo de currency_id
    loan_term = fields.Integer( string = 'Loan Term (Months)', required = True, default = 36)
    rejection_reason = fields.Text( string = 'Rejection Reason', copy=False)
    state = fields.Selection (string = 'Status', selection=[('draft', 'Draft'), ('sent', 'Sent'), ('review', 'Credit Check'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('signed', 'Signed'), ('cancel', 'Canceled')], default='draft', copy = False)
    notes = fields.Html (string = "Notes", copy = False)
    partner_id = fields.Many2one (string = "Customer", required=True, comodel_name='res.partner')
    sale_order_id = fields.Many2one (string = "Related Sale Order", required=True, comodel_name='sale.order')
    user_id = fields.Many2one (string = "Salesperson", required= True, comodel_name = 'res.users')
    product_template_id = fields.Many2one (string = "Product", required = True, comodel_name = 'product.template')
    document_ids = fields.One2many(string = "Documents", comodel_name='loan.application.document', inverse_name='application_id')
    tag_ids = fields.Many2many(string = "Tags", comodel_name='loan.application.tag')


    def action_send(self):
        self.write({'state': 'sent', 'date_application': fields.Date.today()})

    def action_review(self):
        self.write({'state': 'review'})

    def action_approve(self):
        self.write({'state': 'approved', 'date_approval': fields.Date.today()})

    def action_reject(self):
        self.write({'state': 'rejected', 'date_rejection': fields.Date.today()})

    def action_sign(self):
        self.write({'state': 'signed', 'date_signed': fields.Datetime.now()})

    def action_cancel(self):
        self.write({'state': 'cancel'})