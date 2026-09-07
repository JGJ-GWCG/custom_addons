from odoo import models, fields

class LoanTagModel (models.Model):
    _name = 'loan.application.tag'
    _description = 'Categorizes loan applications'

    name = fields.Char(string = "Documents")
    color= fields.Integer(string = "Tags")