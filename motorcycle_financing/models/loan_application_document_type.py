from odoo import models, fields

class LoanAppDocType (models.Model):
    _name = 'loan.application.document.type'
    _description = 'Loan Application Document Type'
    _order = 'name'

    name = fields.Char(string="Documents", required=True, copy=False)
    active = fields.Boolean(default=True, string="Tags")
    document_number = fields.Integer(string="Required Document Number", required=True, default=1)

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'The document type name must be unique.',
        ),
        (
            'document_number_positive',
            'CHECK(document_number > 0)',
            'The required document number must be greater than zero.',
        ),
    ]
