
# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'


from odoo.exceptions import UserError

    def _run_business_checks(self, vals):
        def loc_is_baja(loc):
            return loc and loc.x_estatus_ubicacion == 'baja'
        location = None
        location_dest = None
        if 'location_id' in vals:
            location = self.env['stock.location'].browse(vals['location_id'])
        else:
            location = self.location_id
        if 'location_dest_id' in vals:
            location_dest = self.env['stock.location'].browse(vals['location_dest_id'])
        else:
            location_dest = self.location_dest_id
        if loc_is_baja(location) or loc_is_baja(location_dest):
            raise UserError('No se pueden crear ni modificar movimientos hacia/desde una ubicación en estado Baja.')

# Validación documentos legales para movimientos de armas
# Si el movimiento involucra un producto con tipo de arma definido y la copia legalizada NO está vigente, bloquear.
product = None
if 'product_id' in vals:
    product = self.env['product.product'].browse(vals['product_id'])
else:
    product = self.product_id
if product:
    tmpl = product.product_tmpl_id
    if tmpl.x_tipo_arma and not tmpl.x_copia_legalizada_vigente:
        from odoo.exceptions import UserError
        raise UserError('No puede mover un arma sin copia legalizada vigente.')

    def write(self, vals):
        self._run_business_checks(vals)
        return super().write(vals)

    @api.model
    def create(self, vals):
        # Use sudo where appropriate; but enforce check first
        rec = super().create(vals)
        rec._run_business_checks(vals)
        return rec

    x_ticket_bodega_id = fields.Many2one('bodega.ticket', string='Ticket de bodega')
    x_requerimiento = fields.Selection([
        ('entrega', 'Entrega'),
        ('devolucion', 'Devolución'),
        ('prestamo', 'Préstamo'),
        ('mantenimiento', 'Mantenimiento'),
    ], string='Requerimiento')
    x_no_formulario = fields.Char(string='No. Formulario')
