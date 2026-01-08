from odoo import models, fields

class InventoryEquipment(models.Model):
    _name = 'inventory.equipment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Equipo'

    name = fields.Char(required=True)
    imei = fields.Char()
    state = fields.Selection([
        ('available','Disponible'),
        ('installed','Instalado'),
        ('maintenance','Mantenimiento'),
        ('retired','Baja')
    ], default='available')
