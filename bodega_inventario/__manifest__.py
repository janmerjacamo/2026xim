
# -*- coding: utf-8 -*-
{
    'name': 'Bodega Inventario (Custom)',
    'summary': 'Campos, flujos y automatizaciones para Bodega – Inventario Odoo 17',
    'version': '17.0.1.0.0',
    'category': 'Inventory',
    'author': 'Janmer Jacamo & M365 Copilot',
    'license': 'LGPL-3',
    'website': 'https://example.invalid/bodega_inventario',
    'depends': ['stock', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/stock_lot_views.xml',
        'views/stock_location_views.xml',
        'views/stock_move_views.xml',
        'views/ticket_bodega_views.xml',
        'data/ir_cron.xml',
    ],
    'assets': {},
    'application': False,
    'installable': True,
}
