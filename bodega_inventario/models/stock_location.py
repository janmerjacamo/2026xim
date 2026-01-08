
# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockLocation(models.Model):
    _inherit = 'stock.location'

    x_estatus_ubicacion = fields.Selection([
        ('vigente', 'Vigente'),
        ('baja', 'Baja'),
    ], string='Estatus de ubicación', default='vigente')

    x_fecha_finalizacion = fields.Date(string='Fecha de finalización')
    x_tipo_ubicacion = fields.Selection([
        ('capital', 'Capital'),
        ('departamental', 'Departamental')
    ], string='Tipo de ubicación')
    x_supervisor_responsable = fields.Many2one('hr.employee', string='Supervisor responsable')

