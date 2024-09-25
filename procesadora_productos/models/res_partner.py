from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(
        selection=[
            ('contact', 'Contacto'),
            ('invoice', 'Factura'),
            ('delivery', 'Entrega'),
            ('other', 'Otro'),
            ("private", "Privado"),
        ],
        string='Tipo',
        default='contact',
    )
    phone = fields.Char(string="Telefono")