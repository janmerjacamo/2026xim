
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class BodegaTicket(models.Model):
    _name = 'bodega.ticket'
    _description = 'Ticket de Bodega'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Número de ticket', required=True, copy=False, default=lambda self: _('Nuevo'))
    fecha_hora = fields.Datetime(string='Fecha/Hora', default=fields.Datetime.now)
    depto_solicitante = fields.Many2one('stock.location', string='Departamento solicitante')
    requerimiento = fields.Selection([
        ('entrega', 'Entrega'),
        ('devolucion', 'Devolución'),
        ('prestamo', 'Préstamo'),
        ('mantenimiento', 'Mantenimiento'),
    ], string='Requerimiento')
    descripcion = fields.Text(string='Descripción')
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('procesado', 'Procesado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='borrador', tracking=True)
    no_orden = fields.Char(string='No. Orden')
    no_formulario = fields.Char(string='No. Formulario')
    observaciones = fields.Text(string='Observaciones')
    stock_picking_id = fields.Many2one('stock.picking', string='Transferencia generada')

    def action_aprobar(self):
        self.write({'estado': 'aprobado'})

    def action_generar_picking(self):
        StockPicking = self.env['stock.picking']
        for ticket in self:
            if ticket.stock_picking_id:
                continue
            picking = StockPicking.create({
                'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                'origin': ticket.name,
                'location_id': ticket.depto_solicitante.id if ticket.depto_solicitante else self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_stock').id,
                'note': ticket.descripcion or ''
            })
            ticket.stock_picking_id = picking.id
            ticket.write({'estado': 'procesado'})
            ticket.message_post(body=_('Se generó la transferencia %s desde el ticket.') % picking.name)
