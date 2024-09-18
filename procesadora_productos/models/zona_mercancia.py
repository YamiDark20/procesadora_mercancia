import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ZonaMercancia(models.Model):
    _name = 'zona.mercancia'
    _description = 'Informacion de las mercancia que tiene una zona.'

    mercancia_id = fields.Many2one('empresa.mercancia', string='ID Mercancia', required=True)
    cantidad = fields.Integer(string="Cant. Mercancia", default=0, required=True)
    estado = fields.Selection([
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('danada', 'Dañada'),
    ], string='Estado', copy=False, tracking=True, default='buena')
    zona_almacen_id = fields.Many2one('zona.almacen', string='ID Zona Almacen', required=True)
    
    precio = fields.Float(string='Precio', required=True)
    # sequence_number = fields.Char(string='Secuencia', required=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('empresa.almacen'), readonly=True)

    def update_cantidad(self, cantidad_a_anadir):
        for record in self:
            record.cantidad += cantidad_a_anadir