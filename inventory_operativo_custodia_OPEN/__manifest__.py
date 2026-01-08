{
    "name": "Inventario Operativo y Custodia (OPEN)",
    "version": "16.0.2.1.0",
    "category": "Inventory",
    "summary": "Inventario operativo robusto sin restricciones de seguridad",
    "description": "Gestión completa de armas, equipos, SIM, custodia y tickets visible para todos los usuarios.",
    "author": "XIM Technology",
    "depends": [
        "base",
        "mail",
        "stock"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/menu.xml",
        "views/weapon_views.xml",
        "views/equipment_views.xml",
        "views/sim_views.xml",
        "views/ticket_views.xml",
        "views/custody_views.xml"
    ],
    "application": true
}