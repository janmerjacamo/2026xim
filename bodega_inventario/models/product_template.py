
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Grilletes / Herramientas (estatus)
    x_estatus_operativo = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_uso', 'En uso'),
        ('mantenimiento', 'Mantenimiento'),
        ('baja', 'Baja')
    ], string='Estatus operativo')

    # Armas
    x_tipo_arma = fields.Selection([
        ('pistola', 'Pistola'),
        ('revolver', 'Revólver'),
        ('escopeta', 'Escopeta'),
        ('rifle', 'Rifle'),
        ('otro', 'Otro')
    ], string='Tipo de arma')
    x_calibre = fields.Char(string='Calibre')
    x_tenencia = fields.Char(string='Tenencia')
    x_portacion = fields.Char(string='Portación')
    x_carne_acreditacion = fields.Char(string='Carné de acreditación')
    x_carne_acreditacion_adjunto = fields.Binary(string='Adjunto Carné')
    x_fecha_vencimiento_legal = fields.Date(string='Fecha de vencimiento legal')
    x_municion_x_arma = fields.Integer(string='Munición por arma')
    x_copia_legalizada_vigente = fields.Boolean(string='Copia legalizada vigente')
    x_copia_legalizada_adjunto = fields.Binary(string='Adjunto Copia legalizada')

    # Equipos GPS / IoT
    x_imei = fields.Char(string='IMEI', help='IMEI único del dispositivo', index=True)
    x_placa = fields.Char(string='Placa')
    x_no_factura = fields.Char(string='No. Factura')

    _sql_constraints = [
        ('x_imei_unique', 'unique(x_imei)', 'El IMEI debe ser único.'),
        ('barcode_unique', 'unique(barcode)', 'El código de barras debe ser único.'),
    ]

    # Utilidades
    x_cantidad_en_uso = fields.Integer(
        string='Cantidad en uso',
        compute='_compute_cantidad_en_uso',
        help='Calculado por número de lotes/series asignados a empleados'
    )

    @api.depends('tracking')
    def _compute_cantidad_en_uso(self):
        for product in self:
            if product.tracking in ('lot', 'serial'):
                lot_model = self.env['stock.lot']
                count = lot_model.search_count([
                    ('product_id', '=', product.id),
                    ('x_estatus_activo', '=', 'en_uso')
                ])
                product.x_cantidad_en_uso = count
            else:
                product.x_cantidad_en_uso = 0

    def cron_alerta_vencimiento_legal(self):
        """
        Notifica productos (armas) cuya fecha de vencimiento legal está dentro de 30 días.
        """
        hoy = fields.Date.today()
        limite = hoy + fields.Date.timedelta(days=30)
        productos = self.search([
            ('x_fecha_vencimiento_legal', '!=', False),
            ('x_fecha_vencimiento_legal', '<=', limite),
        ])
        for p in productos:
            p.message_post(body=_('Alerta: vencimiento legal en menos de 30 días (fecha: %s).') % (p.x_fecha_vencimiento_legal))
