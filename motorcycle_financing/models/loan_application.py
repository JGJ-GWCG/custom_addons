from odoo import api, models, fields


class LoanModel(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char(string='Application Number', required=True, copy=False)
    date_application = fields.Date(string='Application Date', readonly=True, copy=False)
    date_approval = fields.Date(string='Approval Date', readonly=True, copy=False)
    date_rejection = fields.Date(string='Rejection Date', readonly=True, copy=False)
    date_signed = fields.Datetime(string='Signed on', readonly=True, copy=False)
    down_payment = fields.Monetary(string='Downpayment', required=True, currency_field='currency_id')  # Relación con el campo de currency_id
    interest_rate = fields.Float(string='Interest Rate (%)', required=True, digits=(5, 2))
    loan_term = fields.Integer(string='Loan Term (Months)', required=True, default=36)
    rejection_reason = fields.Text(string='Rejection Reason', copy=False)
    state = fields.Selection(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('review', 'Credit Check'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('signed', 'Signed'),
            ('cancel', 'Canceled'),
        ],
        default='draft',
        copy=False,
    )
    notes = fields.Html(string="Notes", copy=False)

    sale_order_id = fields.Many2one(string="Related Sale Order", required=True, comodel_name='sale.order')
    product_template_id = fields.Many2one(string="Product", required=True, comodel_name='product.template')
    document_ids = fields.One2many(string="Documents", comodel_name='loan.application.document', inverse_name='application_id')
    tag_ids = fields.Many2many(string="Tags", comodel_name='loan.application.tag')

    # --- Campos espejo de la orden de venta relacionada ---
    # related + store=True: mecanismo nativo de Odoo para "copiar" un campo
    # de otro modelo y mantenerlo sincronizado automáticamente. Quedan de
    # solo lectura por default (Odoo lo hace así en campos related, a menos
    # que se pase readonly=False explícito).

    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        related='sale_order_id.currency_id',
        store=True,
    )

    # Mismas protecciones que se recomendaron desde el inicio para este
    # campo (required, ondelete, index, tracking) — solo cambia CÓMO
    # obtiene su valor (ahora viene de la orden de venta, no se captura a mano).
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name='res.partner',
        related='sale_order_id.partner_id',
        store=True,
        required=True,
        ondelete='restrict',
        index=True,
        tracking=True,  # sin efecto hasta que el modelo herede mail.thread
    )

    user_id = fields.Many2one(
        string="Salesperson",
        comodel_name='res.users',
        related='sale_order_id.user_id',
        store=True,
    )

    sale_order_total = fields.Monetary(string="Sale Order Total", related='sale_order_id.amount_total', store=True)

    # --- Monto del préstamo, derivado del total de la orden y el enganche ---
    loan_amount = fields.Monetary(
        string="Loan Amount",
        compute='_compute_loan_amount',
        store=True,
        # Sin inverse: se decidió que quede de solo lectura para que nunca
        # quede desincronizado del total de la orden y el enganche.
    )

    @api.depends('sale_order_total', 'down_payment')
    def _compute_loan_amount(self):
        for rec in self:
            rec.loan_amount = (rec.sale_order_total or 0.0) - (rec.down_payment or 0.0)

    # --- Contadores de documentos (para smart buttons en el form) ---
    document_count = fields.Integer(
        string="Documents",
        compute='_compute_document_count',
    )

    document_count_approved = fields.Integer(
        string="Approved Documents",
        compute='_compute_document_count_approved',
    )

    @api.depends('document_ids')
    def _compute_document_count(self):
        for rec in self:
            rec.document_count = len(rec.document_ids)

    # OJO: depende de 'document_ids.state', no solo de 'document_ids'.
    # Si solo dijera 'document_ids', este campo NO se recalcularía cuando
    # un documento cambia de 'new' a 'approved' (solo cuando se agregan o
    # quitan documentos) — con 'document_ids.state' sí se recalcula cuando
    # cambia el estado de cualquier documento relacionado.
    @api.depends('document_ids.state')
    def _compute_document_count_approved(self):
        for rec in self:
            rec.document_count_approved = len(
                rec.document_ids.filtered(lambda doc: doc.state == 'approved')
            )

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

    def action_view_documents(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Documents',
            'res_model': 'loan.application.document',
            'view_mode': 'list,form',
            'domain': [('application_id', '=', self.id)],
            'context': {'default_application_id': self.id},
        }
 
    def action_view_documents_approved(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Approved Documents',
            'res_model': 'loan.application.document',
            'view_mode': 'list,form',
            'domain': [('application_id', '=', self.id), ('state', '=', 'approved')],
            'context': {'default_application_id': self.id},
        }
