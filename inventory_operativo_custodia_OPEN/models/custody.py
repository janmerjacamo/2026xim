from odoo import models, fields

class InventoryCustody(models.Model):
    _name = 'inventory.custody'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Custodia'

    employee = fields.Char(required=True)
    weapon_id = fields.Many2one('inventory.weapon')
    equipment_id = fields.Many2one('inventory.equipment')
