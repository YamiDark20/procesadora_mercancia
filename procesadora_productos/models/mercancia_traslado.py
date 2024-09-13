import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MercanciaTraslado(models.Model):
    _name = 'traslado.mercancia'
    _description = 'Informacion de la mercancia que tiene una factura de traslado'

    factura_traslado_id = fields.Many2one('traslado.factura', string='ID Factura', required=True)
    mercancia_id = fields.Many2one('empresa.mercancia', string='ID Mercancia', required=True)

    precio = fields.Float(string='Precio', required=True)

    num_producto = fields.Integer(string="Num. Mercancia", default=0, required=True)
    cant_mercancia = fields.Selection([
        ('por_kilo', 'Por Kilo'),
        ('toneladas', 'Toneladas'),
        ('por_bultos', 'Por Bultos'),
    ], string='Cant. Mercancia', copy=False, tracking=True, default='por_kilo')
    estado = fields.Selection([
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('danada', 'Dañada'),
    ], string='Estado', copy=False, tracking=True, default='buena')