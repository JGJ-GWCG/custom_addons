from odoo import models, fields

class LoanDocModel (models.Model):
    _name = 'loan.application.document'
    _description = 'Tracks required documents for loans.'

    name = fields.Char(string = "Documents")
    application_id = fields.Many2one(string = "Tags", required= True, comodel_name = 'loan.application')
    attachment = fields.Binary(string="File", attachment=True)
    attachment_filename = fields.Char(string="File Name")
    type_id = fields.Many2one (string = "Document Type", required = True, comodel_name = 'loan.application.document.type')
    state = fields.Selection (
        selection=[
            ('new', 'New'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string = "Status",
        required = True,
        default = 'new',
        copy = False,  # para que un documento duplicado no herede el estado "approved"
        tracking = True,   # auditoría: quién aprobó/rechazó y cuándo, clave antes de mandarlo al 3P

    )