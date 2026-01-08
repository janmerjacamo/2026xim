from odoo import models, fields

class InventoryWeapon(models.Model):
    _name = 'inventory.weapon'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Arma'

    name = fields.Char(required=True)
    serial = fields.Char(required=True)
    state = fields.Selection([
        ('available','Disponible'),
        ('assigned','Asignada'),
        ('maintenance','Mantenimiento'),
        ('retired','Baja')
    ], default='available')
