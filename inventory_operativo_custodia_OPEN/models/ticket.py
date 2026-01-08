from odoo import models, fields

class InventoryTicket(models.Model):
    _name = 'inventory.ticket'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Ticket'

    name = fields.Char(default='Nuevo', readonly=True)
    state = fields.Selection([
        ('draft','Borrador'),
        ('approved','Aprobado'),
        ('done','Finalizado')
    ], default='draft')
