from odoo import models, fields

class InventorySIM(models.Model):
    _name = 'inventory.sim'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'SIM'

    number = fields.Char(required=True)
    carrier = fields.Char()
    state = fields.Selection([
        ('free','Libre'),
        ('assigned','Asignada'),
        ('suspended','Suspendida')
    ], default='free')
