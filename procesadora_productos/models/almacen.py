import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Almacen(models.Model):
    _name = 'empresa.almacen'
    _description = 'Informacion del almacen de la empresa'

    sucursal = fields.Char(string='Sucursal', required=True)

    zona_almacen_ids = fields.One2many('zona.almacen', 'almacen_id', string='Id Zona')

    sequence_number = fields.Char(string='Secuencia', required=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('empresa.almacen'), readonly=True)