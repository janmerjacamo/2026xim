
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class StockLot(models.Model):
    _inherit = 'stock.lot'

    x_estatus_activo = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_uso', 'En uso'),
        ('mantenimiento', 'Mantenimiento'),
        ('baja', 'Baja'),
        ('vencido', 'Vencido'),
    ], string='Estatus del activo', default='disponible')

    x_persona_asignada = fields.Many2one('hr.employee', string='Persona asignada')
    x_fecha_asignacion = fields.Date(string='Fecha de asignación')
    x_fecha_estimada_retorno = fields.Date(string='Fecha estimada de retorno')
    x_observaciones = fields.Text(string='Observaciones')

    @api.onchange('x_persona_asignada')
    def _onchange_persona_asignada(self):
        for lot in self:
            lot.x_estatus_activo = 'en_uso' if lot.x_persona_asignada else 'disponible'

    def cron_actualizar_estatus_por_asignacion(self):
        for lot in self.search([]):
            est = 'en_uso' if lot.x_persona_asignada else 'disponible'
            if lot.x_estatus_activo != est:
                lot.x_estatus_activo = est

    def cron_reportar_prestamos_vencidos(self):
        hoy = fields.Date.today()
        vencidos = self.search([
            ('x_fecha_estimada_retorno', '!=', False),
            ('x_fecha_estimada_retorno', '<=', hoy),
            ('x_estatus_activo', '!=', 'disponible')
        ])
        for lot in vencidos:
            lot.message_post(body=_('Préstamo vencido. Fecha estimada de retorno: %s') % lot.x_fecha_estimada_retorno)
